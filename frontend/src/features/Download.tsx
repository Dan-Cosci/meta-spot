// pages/Downloads.tsx
import { useDownload } from "@/hooks/Download";

const STATUS_LABEL: Record<string, string> = {
  pending: "Queued",
  processing: "Downloading",
  done: "Ready",
  failed: "Failed",
};

export default function Downloads() {
  const { jobs, startDownload } = useDownload();

  const active = jobs.filter((j) => j.status === "pending" || j.status === "processing");
  const finished = jobs.filter((j) => j.status === "done" || j.status === "failed");

  return (
    <div className="w-full max-w-4xl text-left">
      {/* Header */}
      <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight md:text-4xl">
            Downloads
          </h1>
          <p className="mt-1 text-sm text-text-muted">
            {jobs.length === 0
              ? "Nothing in progress"
              : `${active.length} in progress · ${finished.length} finished`}
          </p>
        </div>

        <button
          onClick={startDownload}
          disabled={active.length === 0}
          className="btn-animation rounded-xl bg-main px-5 py-2.5 text-sm font-medium text-background disabled:cursor-not-allowed disabled:opacity-40"
        >
          Download all
        </button>
      </header>

      {/* Empty state */}
      {jobs.length === 0 && (
        <div className="rounded-2xl border border-highlight/50 bg-highlight/20 p-12 text-center">
          <p className="text-lg font-medium">No downloads yet</p>
          <p className="mt-1 text-sm text-text-muted">
            Tracks you start downloading will show up here.
          </p>
        </div>
      )}

      {/* Active */}
      {active.length > 0 && (
        <Section title="In progress">
          <ul className="divide-y divide-highlight/40 overflow-hidden rounded-2xl border border-highlight/40 bg-highlight/20">
            {active.map((job) => (
              <Row key={job.song_id}>
                <StatusDot status={job.status} />
                <TrackInfo name={job.name} artist={job.artist} />
                <StatusChip status={job.status} />
              </Row>
            ))}
          </ul>
        </Section>
      )}

      {/* Finished */}
      {finished.length > 0 && (
        <Section title="History">
          <ul className="divide-y divide-highlight/40 overflow-hidden rounded-2xl border border-highlight/40 bg-highlight/20">
            {finished.map((job) => (
              <Row key={job.song_id}>
                <StatusDot status={job.status} />
                <TrackInfo name={job.name} artist={job.artist} />
                <StatusChip status={job.status} />

                {job.status === "done" && (
                  <button className="btn-animation rounded-lg bg-main px-3 py-1.5 text-xs font-medium text-background">
                    Save
                  </button>
                )}
                {job.status === "failed" && (
                  <button className="btn-animation rounded-lg border border-highlight px-3 py-1.5 text-xs font-medium text-text-main hover:bg-card-hover">
                    Retry
                  </button>
                )}
              </Row>
            ))}
          </ul>
        </Section>
      )}
    </div>
  );
}

/* ---- pieces ---- */

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-8">
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-widest text-text-muted">
        {title}
      </h2>
      {children}
    </section>
  );
}

function Row({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex items-center gap-4 px-4 py-3 transition-colors hover:bg-card-hover/40">
      {children}
    </li>
  );
}

function TrackInfo({ name, artist }: { name: string; artist: string }) {
  return (
    <div className="min-w-0 flex-1">
      <p className="truncate font-medium">{name}</p>
      <p className="truncate text-sm text-text-muted">{artist}</p>
    </div>
  );
}

function StatusDot({ status }: { status: string }) {
  const color =
    status === "done"
      ? "bg-main"
      : status === "failed"
      ? "bg-red-500"
      : status === "processing"
      ? "bg-main animate-pulse"
      : "bg-text-muted";

  return <span className={`h-2 w-2 shrink-0 rounded-full ${color}`} />;
}

function StatusChip({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pending: "bg-highlight text-text-muted",
    processing: "bg-main/20 text-main",
    done: "bg-main/20 text-main",
    failed: "bg-red-500/15 text-red-400",
  };

  return (
    <span className={`rounded-full px-3 py-1 text-xs font-medium ${styles[status] ?? styles.pending}`}>
      {STATUS_LABEL[status] ?? status}
    </span>
  );
}
