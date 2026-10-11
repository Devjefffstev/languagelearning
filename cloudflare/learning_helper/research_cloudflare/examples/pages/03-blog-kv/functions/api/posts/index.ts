import * as store from "./_store";

export const onRequestGet: PagesFunction<unknown, { POSTS: KVNamespace }> = async ({ env }) => {
	const posts = await store.list(env.POSTS);
	return Response.json(posts);
};

export const onRequestPost: PagesFunction<unknown, { POSTS: KVNamespace }> = async ({ env, request }) => {
	const input = (await request.json()) as { title: string; body: string };
	const id = crypto.randomUUID();
	const post: store.Post = { id, title: input.title, body: input.body };
	await store.create(env.POSTS, post);
	return Response.json(post, { status: 201 });
};
