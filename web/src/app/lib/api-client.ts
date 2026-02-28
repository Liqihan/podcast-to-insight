import { supabase } from "./supabase";

export async function getAccessToken(): Promise<string | null> {
  if (!supabase) {
    return null;
  }
  const { data } = await supabase.auth.getSession();
  return data.session?.access_token ?? null;
}

export async function authorizedFetch<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAccessToken();
  const headers = new Headers(options.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(url, {
    ...options,
    headers,
  });
  const payload = await response.text();
  if (!response.ok) {
    let detail = "Request failed";
    try {
      const data = JSON.parse(payload) as { detail?: string };
      detail = data.detail ?? detail;
    } catch {
      detail = payload || detail;
    }
    throw new Error(detail || "Request failed");
  }
  if (!payload) {
    return {} as T;
  }
  return JSON.parse(payload) as T;
}
