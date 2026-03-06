const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export async function api(path: string, init?: RequestInit) {
  const res = await fetch(`${API}${path}`, { ...init, credentials: 'include', headers: { 'Content-Type': 'application/json', ...(init?.headers||{}) } });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
