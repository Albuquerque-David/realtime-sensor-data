import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center text-center gap-4">
      <h1 className="text-3xl font-bold">Bem-vindo ao Sensor Data Dashboard</h1>
      <p className="text-lg">Visualize os dados dos sensores em tempo real!</p>
      <Link
        href="/sensors"
        className="bg-purple-700 text-white px-6 py-3 rounded shadow hover:bg-purple-800 transition"
      >
        Ir para os Gráficos
      </Link>
    </div>
  );
}
