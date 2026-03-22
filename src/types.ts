import { z } from '@hono/zod-openapi';

export interface Environment {
  AI: Ai;
}

export const HelloWorldSchema = z
  .object({
    text: z.string(),
  })
  .openapi('User');

export const AIChatRequestSchema = z
  .object({
    message: z.string(),
  })
  .openapi('AIChatRequest');

export const AIChatResponseSchema = z
  .object({
    response: z.string(),
  })
  .openapi('AIChatResponse');

export const AISummarizeRequestSchema = z
  .object({
    text: z.string(),
  })
  .openapi('AISummarizeRequest');

export const AISummarizeResponseSchema = z
  .object({
    summary: z.string(),
  })
  .openapi('AISummarizeResponse');
