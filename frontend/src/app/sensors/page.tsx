"use client";

import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

interface User {
  username: string;
}

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const SensorsPage = () => {
  const [user, setUser] = useState<User | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<string>("24h");
  const [stations, setStations] = useState<any[]>([]);
  const [selectedStation, setSelectedStation] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [currentPage, setCurrentPage] = useState<number>(1);
  const rowsPerPage = 10;

  const [sortColumn, setSortColumn] = useState<string>("equipmentId");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

  const router = useRouter();
  const periods = ["24h", "48h", "1w", "1m"];

  useEffect(() => {
    const token = Cookies.get("token");
    if (!token) {
      router.push("/login");
      return;
    }

    const fetchUser = async () => {
      try {
        console.log(`${process.env.NEXT_PUBLIC_API_URL}`)
        console.log(token)
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) {
          throw new Error("Unauthorized");
        }

        const data = await res.json();
        setUser(data);
      } catch (err) {
        Cookies.remove("token");
        router.push("/login");
      }
    };

    fetchUser();
  }, [router]);

  const fetchStationsData = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = Cookies.get("token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/sensors/averages?period=${selectedPeriod}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!response.ok) {
        throw new Error(`Erro ao buscar dados: ${response.statusText}`);
      }

      const result = await response.json();
      setStations(result);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchStationDetails = async (equipmentId: string) => {
    setLoading(true);
    setError(null);

    try {
      const token = Cookies.get("token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/sensors/${equipmentId}/data?period=${selectedPeriod}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!response.ok) {
        throw new Error(`Erro ao buscar dados: ${response.statusText}`);
      }

      const result = await response.json();
      setSelectedStation(result);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStationsData();
  }, [selectedPeriod]);

  const sortedStations = [...stations].sort((a, b) => {
    const valueA = a[sortColumn];
    const valueB = b[sortColumn];
    if (sortDirection === "asc") {
      return valueA > valueB ? 1 : -1;
    } else {
      return valueA < valueB ? 1 : -1;
    }
  });

  const totalPages = Math.ceil(sortedStations.length / rowsPerPage);
  const paginatedStations = sortedStations.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  const chartData = selectedStation
    ? {
        labels: selectedStation.values.map((v: any) =>
          new Date(v.timestamp).toLocaleTimeString()
        ),
        datasets: [
          {
            label: "Valores",
            data: selectedStation.values.map((v: any) => v.value),
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderWidth: 2,
            tension: 0.4,
          },
        ],
      }
    : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: selectedStation
          ? `Dados da Estação (${selectedStation.equipmentId})`
          : "Selecione uma estação",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  if (!user) return <p>Loading...</p>;

  return (
    <div className="flex gap-8 p-6">
      {/* Tabela */}
      <div className="w-1/3">
        <h1 className="text-2xl font-bold mb-4">Estações</h1>
        <div className="flex justify-center mb-4">
          {periods.map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 mx-2 rounded ${
                selectedPeriod === period ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"
              }`}
            >
              {period.toUpperCase()}
            </button>
          ))}
        </div>
        {loading && <p className="text-center">Carregando...</p>}
        {error && <p className="text-center text-red-500">Erro: {error}</p>}
        {!loading && paginatedStations.length > 0 && (
          <table className="w-full border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-200">
                <th
                  className="border border-gray-300 px-4 py-2 cursor-pointer"
                  onClick={() => handleSort("equipmentId")}
                >
                  Estação {sortColumn === "equipmentId" && (sortDirection === "asc" ? "↑" : "↓")}
                </th>
                <th
                  className="border border-gray-300 px-4 py-2 cursor-pointer"
                  onClick={() => handleSort("average")}
                >
                  Média {sortColumn === "average" && (sortDirection === "asc" ? "↑" : "↓")}
                </th>
                <th className="border border-gray-300 px-4 py-2">Ação</th>
              </tr>
            </thead>
            <tbody>
              {paginatedStations.map((station, index) => (
                <tr key={index}>
                  <td className="border border-gray-300 px-4 py-2">{station.equipmentId}</td>
                  <td className="border border-gray-300 px-4 py-2">
                    {station.average?.toFixed(2) || "N/A"}
                  </td>
                  <td className="border border-gray-300 px-4 py-2 text-center">
                    <button
                      onClick={() => fetchStationDetails(station.equipmentId)}
                      className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                    >
                      🔍
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {/* Paginação */}
        <div className="flex justify-between mt-4">
          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((prev) => prev - 1)}
            className={`px-4 py-2 rounded ${currentPage === 1 ? "bg-gray-300" : "bg-blue-500 text-white"}`}
          >
            Anterior
          </button>
          <span className="px-4 py-2">Página {currentPage} de {totalPages}</span>
          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((prev) => prev + 1)}
            className={`px-4 py-2 rounded ${currentPage === totalPages ? "bg-gray-300" : "bg-blue-500 text-white"}`}
          >
            Próxima
          </button>
        </div>
      </div>

      {/* Gráfico */}
      <div className="w-2/3 h-[500px] bg-white border border-gray-300 rounded-lg p-4">
        {selectedStation && chartData ? (
          <Line options={chartOptions} data={chartData} />
        ) : (
          <p className="text-center">Selecione uma estação para visualizar os dados.</p>
        )}
      </div>
    </div>
  );
};

export default SensorsPage;
