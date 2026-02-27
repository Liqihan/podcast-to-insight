import { create } from "zustand";

type PlayerState = {
  currentTime: number;
  targetTime: number | null;
  setCurrentTime: (time: number) => void;
  seekTo: (time: number) => void;
  clearTarget: () => void;
};

export const usePlayerStore = create<PlayerState>((set) => ({
  currentTime: 0,
  targetTime: null,
  setCurrentTime: (time) => set({ currentTime: time }),
  seekTo: (time) => set({ targetTime: time }),
  clearTarget: () => set({ targetTime: null }),
}));
