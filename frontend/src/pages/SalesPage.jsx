import { useState, useEffect, useCallback } from 'react';
import api from '../api/axios';
import {
  HiOutlineSearch,
  HiOutlineChevronLeft,
  HiOutlineChevronRight,
  HiOutlineFilter,
  HiOutlineX,
} from 'react-icons/hi';

export default function SalesPage() {
  const [salesData, setSalesData] = useState([]);
  const [meta, setMeta] = useState({ total: 0, page: 1, limit: 20, total_pages: 0 });
  const [page, setPage] = useState(1);
  const [limit] = useState(15);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchSales = useCallback(async () => {
    setIsLoading(true);
    try {
      const params = { page, limit };
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;

      const res = await api.get('/', { params });
      setSalesData(res.data.data || []);
      setMeta(res.data.meta || {});
    } catch (error) {
      console.error('Failed to fetch sales:', error);
    }
    setIsLoading(false);
  }, [page, limit, search, statusFilter]);

  useEffect(() => {
    fetchSales();
  }, [fetchSales]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setSearch(searchInput);
  };

  const clearFilters = () => {
    setSearchInput('');
    setSearch('');
    setStatusFilter('');
    setPage(1);
  };

  const formatCurrency = (val) =>
    new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val);

  return (
    <div className="fade-in">
      <h1 className="text-2xl font-bold mb-6">Data Penjualan</h1>

      {/* Filters Bar */}
      <div className="glass-card p-4 mb-6">
        <div className="flex flex-col sm:flex-row gap-3">
          {/* Search */}
          <form onSubmit={handleSearch} className="flex-1">
            <label className="input input-bordered flex items-center gap-2 w-full">
              <HiOutlineSearch className="w-5 h-5 text-base-content/40" />
              <input
                type="text"
                id="sales-search"
                placeholder="Cari produk..."
                className="grow"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
              />
            </label>
          </form>

          {/* Status filter */}
          <select
            id="sales-status-filter"
            className="select select-bordered w-full sm:w-48"
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Semua Status</option>
            <option value="Laris">Laris</option>
            <option value="Tidak">Tidak Laris</option>
          </select>

          {/* Clear */}
          {(search || statusFilter) && (
            <button className="btn btn-ghost btn-sm gap-1" onClick={clearFilters}>
              <HiOutlineX className="w-4 h-4" /> Reset
            </button>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="glass-card overflow-x-auto">
        <table className="table table-zebra">
          <thead>
            <tr className="text-base-content/70">
              <th>#</th>
              <th>Product ID</th>
              <th>Nama Produk</th>
              <th className="text-right">Jumlah Penjualan</th>
              <th className="text-right">Harga</th>
              <th className="text-center">Diskon</th>
              <th className="text-center">Status</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={7} className="text-center py-12">
                  <span className="loading loading-spinner loading-md text-primary"></span>
                </td>
              </tr>
            ) : salesData.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-12 text-base-content/50">
                  <HiOutlineFilter className="w-10 h-10 mx-auto mb-2 opacity-30" />
                  <p>Tidak ada data ditemukan</p>
                </td>
              </tr>
            ) : (
              salesData.map((item, idx) => (
                <tr key={item.id} className="hover transition-colors duration-150">
                  <td className="text-base-content/50 text-sm">
                    {(meta.page - 1) * meta.limit + idx + 1}
                  </td>
                  <td>
                    <span className="font-mono text-xs badge badge-ghost">{item.product_id}</span>
                  </td>
                  <td className="font-medium">{item.product_name}</td>
                  <td className="text-right tabular-nums">{item.jumlah_penjualan.toLocaleString('id-ID')}</td>
                  <td className="text-right tabular-nums">{formatCurrency(item.harga)}</td>
                  <td className="text-center">
                    <span className="badge badge-outline badge-sm">{item.diskon}%</span>
                  </td>
                  <td className="text-center">
                    <span
                      className={`badge badge-sm font-semibold ${
                        item.status === 'Laris'
                          ? 'badge-success text-success-content'
                          : 'badge-error text-error-content'
                      }`}
                    >
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {meta.total_pages > 1 && (
        <div className="flex flex-col sm:flex-row items-center justify-between mt-4 gap-2">
          <p className="text-sm text-base-content/50">
            Menampilkan {(meta.page - 1) * meta.limit + 1}–
            {Math.min(meta.page * meta.limit, meta.total)} dari {meta.total} data
          </p>
          <div className="join">
            <button
              className="join-item btn btn-sm"
              disabled={page <= 1}
              onClick={() => setPage(page - 1)}
              id="sales-prev-page"
            >
              <HiOutlineChevronLeft className="w-4 h-4" />
            </button>
            {Array.from({ length: Math.min(meta.total_pages, 5) }, (_, i) => {
              let pageNum;
              if (meta.total_pages <= 5) {
                pageNum = i + 1;
              } else if (page <= 3) {
                pageNum = i + 1;
              } else if (page >= meta.total_pages - 2) {
                pageNum = meta.total_pages - 4 + i;
              } else {
                pageNum = page - 2 + i;
              }
              return (
                <button
                  key={pageNum}
                  className={`join-item btn btn-sm ${page === pageNum ? 'btn-primary' : ''}`}
                  onClick={() => setPage(pageNum)}
                >
                  {pageNum}
                </button>
              );
            })}
            <button
              className="join-item btn btn-sm"
              disabled={page >= meta.total_pages}
              onClick={() => setPage(page + 1)}
              id="sales-next-page"
            >
              <HiOutlineChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
