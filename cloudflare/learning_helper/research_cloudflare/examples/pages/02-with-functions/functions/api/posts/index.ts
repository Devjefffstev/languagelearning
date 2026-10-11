import { posts } from "./_store";

export const onRequestGet: PagesFunction = async () => {
	return Response.json(posts);
};

export const onRequestPost: PagesFunction = async ({ request }) => {
	const { title, body } = (await request.json()) as { title: string; body: string };
	const id = String(posts.length + 1);
	posts.push({ id, title, body });
	return Response.json({ id, title, body }, { status: 201 });
};
