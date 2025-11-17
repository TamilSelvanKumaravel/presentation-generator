import { useMemo, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8000";

const defaultForm = {
  topic: "",
  numberOfSlides: 5,
  format: "pptx",
  style: "professional",
  language: "English",
  includeImages: false,
};

const styles = [
  { value: "professional", label: "Professional" },
  { value: "casual", label: "Casual" },
  { value: "academic", label: "Academic" },
];

function App() {
  const [form, setForm] = useState(defaultForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const downloadUrl = useMemo(() => {
    if (!result?.download_url) return "";
    if (result.download_url.startsWith("http")) {
      return result.download_url;
    }
    return `${API_BASE_URL}${result.download_url}`;
  }, [result, API_BASE_URL]);

  const handleChange = (field) => (event) => {
    const value =
      event.target.type === "checkbox"
        ? event.target.checked
        : event.target.value;

    setForm((prev) => ({
      ...prev,
      [field]:
        field === "numberOfSlides" ? Number(value) || defaultForm.numberOfSlides : value,
    }));
  };

  const handleReset = () => {
    setForm(defaultForm);
    setResult(null);
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!form.topic.trim()) {
      setError("Topic is required.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/presentation/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: form.topic,
          number_of_slides: form.numberOfSlides,
          format: form.format,
          style: form.style,
          language: form.language,
          include_images: form.includeImages,
        }),
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody?.detail || "Failed to generate presentation.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-10">
        <header className="space-y-4 text-center md:text-left">
          <p className="text-sm font-semibold uppercase text-indigo-400 tracking-wider">
            Presentation Generator
          </p>
          <h1 className="text-3xl font-bold text-white md:text-4xl">
            Turn ideas into polished slide decks with AI
          </h1>
          <p className="text-slate-300 md:max-w-3xl">
            Describe your topic, choose a style, and let the LLM craft a complete presentation.
            Downloads are delivered as PPTX files ready for PowerPoint or Google Slides import.
          </p>
        </header>

        <main className="mt-10 grid flex-1 gap-8 md:grid-cols-[1.4fr,1fr]">
          <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl shadow-indigo-500/5">
            <form className="space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-2">
                <label htmlFor="topic" className="block text-sm font-medium text-slate-200">
                  Presentation topic <span className="text-pink-400">*</span>
                </label>
                <textarea
                  id="topic"
                  name="topic"
                  rows={5}
                  value={form.topic}
                  onChange={handleChange("topic")}
                  placeholder="e.g. How generative AI is transforming product design"
                  className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-base text-slate-100 placeholder:text-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
                />
              </div>

              <div className="grid gap-6 md:grid-cols-2">
                <div className="space-y-2">
                  <label htmlFor="numberOfSlides" className="block text-sm font-medium text-slate-200">
                    Number of slides
                  </label>
                  <input
                    id="numberOfSlides"
                    type="number"
                    min={1}
                    max={50}
                    value={form.numberOfSlides}
                    onChange={handleChange("numberOfSlides")}
                    className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-base text-slate-100 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="style" className="block text-sm font-medium text-slate-200">
                    Presentation style
                  </label>
                  <select
                    id="style"
                    value={form.style}
                    onChange={handleChange("style")}
                    className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-base text-slate-100 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
                  >
                    {styles.map((style) => (
                      <option key={style.value} value={style.value}>
                        {style.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-2">
                  <label htmlFor="language" className="block text-sm font-medium text-slate-200">
                    Language
                  </label>
                  <input
                    id="language"
                    type="text"
                    value={form.language}
                    onChange={handleChange("language")}
                    className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-base text-slate-100 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="format" className="block text-sm font-medium text-slate-200">
                    Output format
                  </label>
                  <select
                    id="format"
                    value={form.format}
                    onChange={handleChange("format")}
                    className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-base text-slate-100 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
                  >
                    <option value="pptx">PowerPoint (.pptx)</option>
                    <option value="google-slides" disabled>
                      Google Slides (coming soon)
                    </option>
                  </select>
                </div>
              </div>

              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={form.includeImages}
                  onChange={handleChange("includeImages")}
                  className="h-5 w-5 rounded border border-slate-700 bg-slate-900 text-indigo-500 focus:ring-indigo-500/60"
                />
                <span className="text-sm text-slate-300">
                  Suggest relevant image prompts for each slide
                </span>
              </label>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center justify-center rounded-xl bg-indigo-500 px-6 py-3 text-base font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  {loading ? "Generating..." : "Generate presentation"}
                </button>
                <button
                  type="button"
                  onClick={handleReset}
                  className="inline-flex items-center justify-center rounded-xl border border-slate-700 px-6 py-3 text-base font-semibold text-slate-200 transition hover:bg-slate-800"
                >
                  Reset
                </button>
              </div>

              {error && (
                <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-100">
                  {error}
                </div>
              )}
            </form>
          </section>

          <aside className="flex flex-col gap-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-indigo-500/10">
              <h2 className="text-lg font-semibold text-white">How it works</h2>
              <ol className="mt-4 space-y-3 text-sm text-slate-300">
                <li className="flex gap-3">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500 text-xs font-semibold text-white">
                    1
                  </span>
                  Describe your narrative and key takeaways.
                </li>
                <li className="flex gap-3">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500 text-xs font-semibold text-white">
                    2
                  </span>
                  The backend LLM drafts slide-by-slide bullet points.
                </li>
                <li className="flex gap-3">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500 text-xs font-semibold text-white">
                    3
                  </span>
                  A Python service renders a PPTX ready for download.
                </li>
              </ol>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-indigo-500/10">
              <h2 className="text-lg font-semibold text-white">Generation result</h2>
              {!result && !loading && (
                <p className="mt-3 text-sm text-slate-400">
                  Submit a topic to see the download link and request metadata.
                </p>
              )}

              {loading && (
                <div className="mt-4 flex items-center gap-3 text-sm text-slate-300">
                  <span className="h-3 w-3 animate-ping rounded-full bg-indigo-400" />
                  Drafting slides with the LLM…
                </div>
              )}

              {result && (
                <dl className="mt-4 space-y-3 text-sm text-slate-200">
                  <div>
                    <dt className="text-slate-400">Status</dt>
                    <dd className="font-medium text-emerald-400">
                      {result.success ? "Completed" : "Failed"}
                    </dd>
                  </div>
                  {result.file_path && (
                    <div>
                      <dt className="text-slate-400">File path</dt>
                      <dd className="break-all text-slate-100">{result.file_path}</dd>
                    </div>
                  )}
                  {downloadUrl && (
      <div>
                      <dt className="text-slate-400">Download</dt>
                      <dd>
                        <a
                          href={downloadUrl}
                          className="inline-flex items-center gap-2 rounded-lg bg-emerald-500 px-4 py-2 font-semibold text-emerald-950 transition hover:bg-emerald-400"
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Download PPTX
                          <span aria-hidden="true">↗</span>
                        </a>
                      </dd>
                    </div>
                  )}
                  {result.message && (
                    <div>
                      <dt className="text-slate-400">Message</dt>
                      <dd>{result.message}</dd>
                    </div>
                  )}
                </dl>
              )}
            </div>
          </aside>
        </main>

        <footer className="mt-10 border-t border-slate-800 pt-6 text-xs text-slate-500">
          Backend hosted at{" "}
          <code className="rounded bg-slate-800 px-2 py-1 text-indigo-300">
            {API_BASE_URL}
          </code>
          . Update <code>VITE_API_BASE_URL</code> to point at another instance.
        </footer>
      </div>
      </div>
  );
}

export default App;
