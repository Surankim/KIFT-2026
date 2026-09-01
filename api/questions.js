// api/questions.js
//
// Vercel 서버리스 함수: Q&A 데이터를 Upstash Redis에 저장/조회합니다.
// Redis Hash 구조를 써서, 질문마다 별도 필드로 저장 -> 동시에 여러 명이
// 제출해도 서로 덮어쓰지 않습니다 (HSET은 필드 단위로 원자적입니다).
//
// 필요한 환경변수 (Vercel 대시보드 > Settings > Environment Variables):
//   KV_REST_API_URL
//   KV_REST_API_TOKEN
// -> Vercel 프로젝트에서 "Storage" 탭 > Upstash Redis 연결하면 자동으로 채워집니다.
// (실제 생성되는 변수 이름은 연결 방식에 따라 KV_REST_API_* 또는
//  UPSTASH_REDIS_REST_* 로 다를 수 있어, 두 가지 다 확인하도록 처리했습니다.)

const REDIS_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const REDIS_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const HASH_KEY = 'kift2026:qa';

async function redis(command) {
  const res = await fetch(REDIS_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${REDIS_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(command),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Redis error: ${res.status} ${text}`);
  }
  const data = await res.json();
  return data.result;
}

module.exports = async function handler(req, res) {
  // CORS - 사이트 도메인에서 fetch 가능하게
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    if (req.method === 'GET') {
      // 전체 질문 목록 조회
      const raw = await redis(['HGETALL', HASH_KEY]);
      const items = [];
      for (let i = 0; i < raw.length; i += 2) {
        try {
          items.push(JSON.parse(raw[i + 1]));
        } catch (e) { /* skip broken entry */ }
      }
      items.sort((a, b) => b.time - a.time);
      return res.status(200).json({ questions: items });
    }

    if (req.method === 'POST') {
      // 새 질문 추가
      const { text, name } = req.body || {};
      if (!text || typeof text !== 'string' || !text.trim()) {
        return res.status(400).json({ error: 'text is required' });
      }
      const id = Date.now() + '_' + Math.random().toString(36).slice(2, 8);
      const question = {
        id,
        text: text.trim().slice(0, 500),
        name: (name || '').trim().slice(0, 60),
        time: Date.now(),
        read: false,
      };
      await redis(['HSET', HASH_KEY, id, JSON.stringify(question)]);
      return res.status(200).json({ ok: true, question });
    }

    if (req.method === 'PATCH') {
      // 읽음 상태 토글
      const { id, read } = req.body || {};
      if (!id) return res.status(400).json({ error: 'id is required' });
      const raw = await redis(['HGET', HASH_KEY, id]);
      if (!raw) return res.status(404).json({ error: 'not found' });
      const question = JSON.parse(raw);
      question.read = !!read;
      await redis(['HSET', HASH_KEY, id, JSON.stringify(question)]);
      return res.status(200).json({ ok: true, question });
    }

    if (req.method === 'DELETE') {
      const { id, all } = req.body || {};
      if (all) {
        // 전체 삭제
        await redis(['DEL', HASH_KEY]);
        return res.status(200).json({ ok: true, cleared: true });
      }
      if (!id) return res.status(400).json({ error: 'id is required' });
      // 개별 질문 삭제
      await redis(['HDEL', HASH_KEY, id]);
      return res.status(200).json({ ok: true, deleted: id });
    }

    return res.status(405).json({ error: 'method not allowed' });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'server error' });
  }
};
