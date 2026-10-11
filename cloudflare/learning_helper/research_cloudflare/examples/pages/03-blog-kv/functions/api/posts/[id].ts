import * as store from "./_store";

export const onRequestGet: PagesFunction<unknown, { POSTS: KVNamespace }> = async ({ env, params }) => {
	const post = await store.get(env.POSTS, params.id);
	if (!post) return new Response("Not Found", { status: 404 });
	return Response.json(post);
};

export const onRequestDelete: PagesFunction<unknown, { POSTS: KVNamespace }> = async ({ env, params }) => {
	const ok = await store.remove(env.POSTS, params.id);
	if (!ok) return new Response("Not Found", { status: 404 });
	return new Response(null, { status: 204 });
};
