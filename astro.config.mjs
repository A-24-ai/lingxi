import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 部署地址占位，等确认 GitHub 仓库后替换为实际地址
export default defineConfig({
  site: 'https://A-24-ai.github.io/entrepreneur-thoughts/',
  integrations: [sitemap()],
});
