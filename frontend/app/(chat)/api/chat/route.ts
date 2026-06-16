export async function POST(req: Request) {
  try {
    // Parse the incoming request body
    const { query } = await req.json();

    // Forward the query to your FastAPI backend
    const response = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    // Parse backend response
    const data = await response.json();

    // Return it back to the frontend
    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error in chat route:", error);
    return new Response(
      JSON.stringify({ error: "Backend connection failed" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
