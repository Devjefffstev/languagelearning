import { posts } from "./_store";

export const onRequestGet: PagesFunction<{ id: string }> = async ({ params }) => {
	const post = posts.find((p) => p.id === params.id);
	if (!post) return new Response("Not Found", { status: 404 });
	return Response.json(post);
};

export const onRequestDelete: PagesFunction<{ id: string }> = async ({ params }) => {
	const idx = posts.findIndex((p) => p.id === params.id);
	if (idx < 0) return new Response("Not Found", { status: 404 });
	posts.splice(idx, 1);
	return new Response(null, { status: 204 });
};
