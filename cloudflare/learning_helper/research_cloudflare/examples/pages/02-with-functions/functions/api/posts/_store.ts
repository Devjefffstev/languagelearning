export interface Post {
	id: string;
	title: string;
	body: string;
}

export const posts: Post[] = [
	{ id: "1", title: "Hello, World", body: "First post." },
	{ id: "2", title: "Pages Functions", body: "Just Workers with a routing convention." },
];
