export type TraceEvent = {
  name: string;
  is_valid?: boolean;
  retries?: number;
};

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  traces?: TraceEvent[];
  thread_id?: string;
};
