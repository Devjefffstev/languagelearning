export function time() {
	return Response.json({
		now: new Date().toISOString(),
		timestamp: Date.now(),
	});
}
