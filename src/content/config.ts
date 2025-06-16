import { defineCollection, z } from 'astro:content';

const namesCollection = defineCollection({
  type: 'data',
  schema: z.object({
    domain: z.string(),
    name: z.string(),
    title: z.string().max(80).optional(),
    url: z.string().url().optional(),
    email: z.string().email().optional(),
    github: z.string().optional(),
    candidate: z.boolean().optional(),
    invalid: z.boolean().optional(),
  }).refine(
    (data) => {
      // If not a candidate, title is required
      if (!data.candidate) {
        return !!data.title;
      }
      return true;
    },
    {
      message: "Title is required for non-candidates",
      path: ["title"],
    }
  ),
});

// Export the collections
export const collections = {
  'names': namesCollection,
};
