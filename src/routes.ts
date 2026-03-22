import { createRoute } from '@hono/zod-openapi';
import {
  AIChatRequestSchema,
  AIChatResponseSchema,
  AISummarizeRequestSchema,
  AISummarizeResponseSchema,
  HelloWorldSchema,
} from './types';

export const HelloWorldRoute = createRoute({
  method: 'get',
  path: '/',
  request: {},
  responses: {
    200: {
      content: { 'application/json': { schema: HelloWorldSchema } },
      description: 'Hello World',
    },
  },
});

export const AIChatRoute = createRoute({
  method: 'post',
  path: '/ai/chat',
  request: {
    body: {
      content: { 'application/json': { schema: AIChatRequestSchema } },
      required: true,
    },
  },
  responses: {
    200: {
      content: { 'application/json': { schema: AIChatResponseSchema } },
      description: 'AI chat response',
    },
  },
});

export const AISummarizeRoute = createRoute({
  method: 'post',
  path: '/ai/summarize',
  request: {
    body: {
      content: { 'application/json': { schema: AISummarizeRequestSchema } },
      required: true,
    },
  },
  responses: {
    200: {
      content: { 'application/json': { schema: AISummarizeResponseSchema } },
      description: 'AI summarization response',
    },
  },
});
