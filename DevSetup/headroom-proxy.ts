/**
 * Headroom Extension for Pi Coding Agent
 *
 * Routes requests through local Headroom context-compression proxy,
 * reducing token costs by 30-60%. Also registers the headroom_retrieve
 * tool for CCR (Cache-Compress-Retrieve) support.
 *
 * Usage:
 *   pi --extension pi-headroom
 *   pi -e ~/ws/pi-headroom
 *
 * Headroom proxy must be running (default: localhost:8787).
 * Start with: hpi --stop && hpi
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";

export interface HeadroomConfig {
  port: number;
  host: string;
  /** Override the upstream API URL the proxy forwards to */
  upstreamUrl?: string;
  /** Whether to register the headroom_retrieve tool */
  registerRetrieveTool: boolean;
}

const DEFAULT_CONFIG: HeadroomConfig = {
  port: 8787,
  host: "localhost",
  registerRetrieveTool: true,
};

function getBaseUrl(config: HeadroomConfig): string {
  return `http://${config.host}:${config.port}/v1`;
}

async function loadConfig(cwd: string): Promise<HeadroomConfig> {
  const { readFile } = await import("node:fs/promises");
  const { resolve } = await import("node:path");
  const { homedir } = await import("node:os");

  const paths = [
    resolve(cwd, ".pi", "headroom-config.json"),
    resolve(homedir(), ".pi", "agent", "headroom-config.json"),
  ];

  for (const configPath of paths) {
    try {
      const content = await readFile(configPath, "utf-8");
      const parsed = JSON.parse(content) as Partial<HeadroomConfig>;
      return { ...DEFAULT_CONFIG, ...parsed };
    } catch {
      // Try next path
    }
  }

  return DEFAULT_CONFIG;
}

async function isProxyRunning(host: string, port: number): Promise<boolean> {
  try {
    const response = await fetch(`http://${host}:${port}/health`, {
      signal: AbortSignal.timeout(2000),
    });
    return response.ok;
  } catch {
    return false;
  }
}

export default async function headroomExtension(pi: ExtensionAPI) {
  let config = DEFAULT_CONFIG;

  pi.on("session_start", async (_event, ctx) => {
    try {
      config = await loadConfig(ctx.cwd || process.cwd());
    } catch {
      config = DEFAULT_CONFIG;
    }

    const baseUrl = getBaseUrl(config);
    const running = await isProxyRunning(config.host, config.port);

    if (running) {
      // Override opencode-go to route through Headroom compression proxy
      pi.registerProvider("opencode-go", {
        baseUrl,
      });

      if (ctx.hasUI) {
        ctx.ui.notify(
          `Headroom: proxy active on :${config.port} (30-60% savings)`,
          "info"
        );
      }
    } else {
      if (ctx.hasUI) {
        ctx.ui.notify(
          `Headroom: proxy not running on :${config.port}, using direct connection`,
          "warning"
        );
      }
    }
  });

  // Register headroom_retrieve tool for CCR support
  if (config.registerRetrieveTool) {
    pi.registerTool({
      name: "headroom_retrieve",
      label: "Headroom Retrieve",
      description:
        "Retrieve original content that was compressed by Headroom. " +
        "Use when you need full detail about something that was summarized.",
      promptSnippet:
        "Retrieve compressed context detail from Headroom cache",
      parameters: Type.Object({
        hash: Type.String({
          description: "Hash identifier for the compressed content to retrieve",
        }),
        query: Type.Optional(
          Type.String({
            description: "Optional search query to filter retrieved content",
          })
        ),
      }),
      async execute(
        toolCallId: string,
        params: { hash: string; query?: string },
        signal: AbortSignal | undefined,
        _onUpdate: any,
        _ctx: any
      ) {
        const retrieveUrl = `http://${config.host}:${config.port}/v1/retrieve/tool_call`;

        try {
          const body = {
            tool_call: {
              id: toolCallId,
              name: "headroom_retrieve",
              input: {
                hash: params.hash,
                query: params.query || null,
              },
            },
          };

          const response = await fetch(retrieveUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
            signal,
          });

          if (!response.ok) {
            const errorText = await response.text();
            return {
              content: [
                {
                  type: "text",
                  text: `Retrieval failed (${response.status}): ${errorText}`,
                },
              ],
              isError: true,
            };
          }

          const data = await response.json();

          // The proxy returns a tool_result format
          if (data.tool_result) {
            return {
              content: data.tool_result.content || [
                { type: "text", text: JSON.stringify(data) },
              ],
            };
          }

          return {
            content: [
              {
                type: "text",
                text: typeof data === "string" ? data : JSON.stringify(data),
              },
            ],
          };
        } catch (error: any) {
          return {
            content: [
              {
                type: "text",
                text: `Retrieval error: ${error?.message || String(error)}`,
              },
            ],
            isError: true,
          };
        }
      },
    });
  }
}
