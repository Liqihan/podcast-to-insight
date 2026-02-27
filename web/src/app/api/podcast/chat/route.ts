import { NextRequest, NextResponse } from "next/server";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function POST(request: NextRequest) {
  const body = await request.json();
  const auth = request.headers.get("authorization");
  const response = await fetch(`${API_BASE}/api/v1/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(auth ? { Authorization: auth } : {}),
    },
    body: JSON.stringify(body),
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
