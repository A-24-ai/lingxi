import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    // 文章标题
    title: z.string(),
    // 摘要（用于列表与SEO description）
    description: z.string().default(''),
    // 栏目：赚钱与生意 / 个人成长 / 情绪价值 / 行业分析 / 职场生存 / 经营故事 / 时事观察
    category: z.string().default('赚钱与生意'),
    // 发布时间
    date: z.coerce.date(),
    // 封面图（public目录下的路径，可选）
    coverImage: z.string().optional(),
    // 标签
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { posts };
