export function user(params: Record<string, string>) {
	return Response.json({
		id: params.id,
		name: `User ${params.id}`,
	});
}
