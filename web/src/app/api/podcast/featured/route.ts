import { NextRequest, NextResponse } from "next/server";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function GET(request: NextRequest) {
  const auth = request.headers.get("authorization");
  const { searchParams } = new URL(request.url);
  const limit = searchParams.get("limit");
  const query = limit ? `?limit=${encodeURIComponent(limit)}` : "";

  const response = await fetch(`${API_BASE}/api/v1/episodes/featured${query}`, {
    headers: {
      ...(auth ? { Authorization: auth } : {}),
    },
  });
  const payload = await response.text();
  let json: unknown;
  try {
    json = JSON.parse(payload);
  } catch {
    json = { detail: payload };
  }
  return NextResponse.json(json, { status: response.status });
}
