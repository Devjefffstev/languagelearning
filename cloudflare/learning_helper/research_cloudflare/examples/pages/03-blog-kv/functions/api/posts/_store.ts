export interface Post {
	id: string;
	title: string;
	body: string;
}

export async function list(posts: KVNamespace): Promise<Post[]> {
	const list = await posts.list();
	const items = await Promise.all(
		list.keys.map(async (k) => {
			const raw = await posts.get(k.name);
			return raw ? (JSON.parse(raw) as Post) : null;
		}),
	);
	return items.filter((x): x is Post => x !== null);
}

export async function get(posts: KVNamespace, id: string): Promise<Post | null> {
	const raw = await posts.get(id);
	return raw ? (JSON.parse(raw) as Post) : null;
}

export async function create(posts: KVNamespace, post: Post): Promise<void> {
	await posts.put(post.id, JSON.stringify(post));
}

export async function remove(posts: KVNamespace, id: string): Promise<boolean> {
	const existing = await posts.get(id);
	if (!existing) return false;
	await posts.delete(id);
	return true;
}
