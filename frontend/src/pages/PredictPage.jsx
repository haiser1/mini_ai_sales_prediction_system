import { useState } from 'react';
import api from '../api/axios';
import {
  HiOutlineChartBar,
  HiOutlineCurrencyDollar,
  HiOutlineTag,
  HiOutlineShoppingCart,
  HiOutlineCheckCircle,
  HiOutlineXCircle,
} from 'react-icons/hi';

export default function PredictPage() {
  const [jumlahPenjualan, setJumlahPenjualan] = useState('');
  const [harga, setHarga] = useState('');
  const [diskon, setDiskon] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setIsLoading(true);
    try {
      const res = await api.post('/predict', {
        jumlah_penjualan: parseInt(jumlahPenjualan),
        harga: parseInt(harga),
        diskon: parseInt(diskon),
      });
      setResult(res.data.data.laris);
    } catch (err) {
      const message = err.response?.data?.message || 'Prediksi gagal';
      setError(message);
    }
    setIsLoading(false);
  };

  const resetForm = () => {
    setJumlahPenjualan('');
    setHarga('');
    setDiskon('');
    setResult(null);
    setError('');
  };

  const isLaris = result === 'Laris';

  return (
    <div className="max-w-2xl mx-auto fade-in">
      <h1 className="text-2xl font-bold mb-6">Prediksi Penjualan</h1>

      <div className="grid gap-6">
        {/* Predict Form */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <HiOutlineChartBar className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="font-bold">Input Data Produk</h2>
              <p className="text-xs text-base-content/50">Masukkan data untuk prediksi apakah produk laris atau tidak</p>
            </div>
          </div>

          {error && (
            <div className="alert alert-error mb-4 text-sm fade-in">
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label">
                <span className="label-text font-semibold flex items-center gap-2">
                  <HiOutlineShoppingCart className="w-4 h-4" /> Jumlah Penjualan
                </span>
              </label>
              <input
                type="number"
                id="predict-jumlah"
                className="input input-bordered w-full"
                placeholder="Contoh: 150"
                value={jumlahPenjualan}
                onChange={(e) => setJumlahPenjualan(e.target.value)}
                min={0}
                required
              />
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-semibold flex items-center gap-2">
                  <HiOutlineCurrencyDollar className="w-4 h-4" /> Harga Produk (Rp)
                </span>
              </label>
              <input
                type="number"
                id="predict-harga"
                className="input input-bordered w-full"
                placeholder="Contoh: 50000"
                value={harga}
                onChange={(e) => setHarga(e.target.value)}
                min={0}
                required
              />
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-semibold flex items-center gap-2">
                  <HiOutlineTag className="w-4 h-4" /> Diskon (%)
                </span>
              </label>
              <input
                type="number"
                id="predict-diskon"
                className="input input-bordered w-full"
                placeholder="0 - 100"
                value={diskon}
                onChange={(e) => setDiskon(e.target.value)}
                min={0}
                max={100}
                required
              />
              <label className="label">
                <span className="label-text-alt text-base-content/40">Masukkan nilai 0 sampai 100</span>
              </label>
            </div>

            <div className="flex gap-2 pt-2">
              <button
                type="submit"
                id="predict-submit"
                className="btn btn-primary flex-1"
                disabled={isLoading}
              >
                {isLoading ? (
                  <span className="loading loading-spinner loading-sm"></span>
                ) : (
                  <>
                    <HiOutlineChartBar className="w-5 h-5" /> Prediksi
                  </>
                )}
              </button>
              <button type="button" className="btn btn-ghost" onClick={resetForm}>
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Result Card */}
        {result && (
          <div
            className={`glass-card p-6 text-center slide-up border-2 ${
              isLaris ? 'border-success/40' : 'border-error/40'
            }`}
          >
            <div
              className={`inline-flex items-center justify-center w-20 h-20 rounded-full mb-4 ${
                isLaris ? 'bg-success/10' : 'bg-error/10'
              }`}
            >
              {isLaris ? (
                <HiOutlineCheckCircle className="w-12 h-12 text-success" />
              ) : (
                <HiOutlineXCircle className="w-12 h-12 text-error" />
              )}
            </div>
            <h2 className="text-2xl font-bold mb-2">
              Produk Diprediksi{' '}
              <span className={isLaris ? 'text-success' : 'text-error'}>{result}</span>
            </h2>
            <p className="text-base-content/60 text-sm">
              {isLaris
                ? 'Produk ini memiliki potensi penjualan yang baik berdasarkan data yang diberikan.'
                : 'Produk ini diprediksi kurang diminati. Pertimbangkan untuk menyesuaikan strategi harga/diskon.'}
            </p>

            {/* Input Summary */}
            <div className="mt-4 flex justify-center gap-4 flex-wrap">
              <div className="badge badge-lg badge-outline gap-1">
                <HiOutlineShoppingCart className="w-3 h-3" /> {parseInt(jumlahPenjualan).toLocaleString('id-ID')} unit
              </div>
              <div className="badge badge-lg badge-outline gap-1">
                <HiOutlineCurrencyDollar className="w-3 h-3" /> Rp {parseInt(harga).toLocaleString('id-ID')}
              </div>
              <div className="badge badge-lg badge-outline gap-1">
                <HiOutlineTag className="w-3 h-3" /> Diskon {diskon}%
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
