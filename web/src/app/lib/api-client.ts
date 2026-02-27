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
  if (!response.ok) {
    let detail = "Request failed";
    try {
      const data = await response.json();
      detail = (data as { detail?: string }).detail ?? detail;
    } catch {
      detail = await response.text();
    }
    throw new Error(detail || "Request failed");
  }
  return response.json() as Promise<T>;
}
