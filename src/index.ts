import type { Environment } from './types';
import { OpenAPIHono } from '@hono/zod-openapi';
import { logger } from 'hono/logger';
import { poweredBy } from 'hono/powered-by';
import { AIChatRoute, AISummarizeRoute, HelloWorldRoute } from './routes';

const app = new OpenAPIHono<{ Bindings: Environment }>();
app.use(poweredBy());
app.use(logger());
app.openapi(HelloWorldRoute, c => {
  return c.json({ text: 'Hello Hono!' });
});

app.openapi(AIChatRoute, async c => {
  const { message } = c.req.valid('json');
  const result = await c.env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      {
        role: 'system',
        content:
          'You are a helpful assistant. Provide concise and accurate responses.',
      },
      { role: 'user', content: message },
    ],
  });
  return c.json({ response: (result as { response: string }).response });
});

app.openapi(AISummarizeRoute, async c => {
  const { text } = c.req.valid('json');
  const result = await c.env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      {
        role: 'system',
        content:
          'You are a summarization assistant. Summarize the following text concisely while preserving the key points.',
      },
      { role: 'user', content: text },
    ],
  });
  return c.json({ summary: (result as { response: string }).response });
});

app.doc('/docs', {
  openapi: '3.0.0',
  info: {
    version: '1.0.0',
    title: 'My API',
  },
});
export default app;
