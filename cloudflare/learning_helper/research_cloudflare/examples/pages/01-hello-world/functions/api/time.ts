export const onRequestGet: PagesFunction = async () => {
	return Response.json({
		now: new Date().toISOString(),
		timestamp: Date.now(),
	});
};
