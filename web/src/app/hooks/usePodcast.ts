import useSWR from "swr";

import { authorizedFetch } from "../lib/api-client";

export function usePodcast(episodeId?: string, summaryId?: string) {
  const normalizedSummaryId =
    summaryId && summaryId !== "undefined" && summaryId !== "null" ? summaryId : undefined;

  const { data: status, error: statusError } = useSWR(
    normalizedSummaryId ? `/api/podcast/status/${normalizedSummaryId}` : null,
    (url: string) => authorizedFetch(url),
    { refreshInterval: 3000 }
  );

  const { data: episode, error: episodeError } = useSWR(
    episodeId ? `/api/podcast/episode/${episodeId}` : null,
    (url: string) => authorizedFetch(url)
  );

  return {
    status,
    episode,
    isLoading: (!status && !!summaryId) || (!episode && !!episodeId),
    isError: statusError || episodeError,
  };
}
