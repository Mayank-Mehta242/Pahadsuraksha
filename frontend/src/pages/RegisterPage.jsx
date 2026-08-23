import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { UserPlus } from "lucide-react";
import { useAuth } from "../hooks/useAuth.js";
import { mockDistricts } from "../data/mockData.js";

const initialForm = {
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  district: "",
  role: "driver",
  phone: "",
};

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    try {
      await register(form);
      toast.success("Account created!");
      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] contour-surface flex items-center justify-center px-4 py-16">
      <div className="glass-panel w-full max-w-lg p-8">
        <h1 className="text-2xl font-display font-bold text-white mb-1">Create your account</h1>
        <p className="text-sm text-slate-200 mb-8">Get location-aware landslide alerts for your district.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-200 mb-1.5 block">Full name</label>
              <input
                required
                className="input-field"
                value={form.name}
                onChange={(e) => update("name", e.target.value)}
              />
            </div>
            <div>
              <label className="text-xs text-slate-200 mb-1.5 block">Email</label>
              <input
                type="email"
                required
                className="input-field"
                value={form.email}
                onChange={(e) => update("email", e.target.value)}
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-200 mb-1.5 block">Password</label>
              <input
                type="password"
                required
                className="input-field"
                value={form.password}
                onChange={(e) => update("password", e.target.value)}
              />
            </div>
            <div>
              <label className="text-xs text-slate-200 mb-1.5 block">Confirm password</label>
              <input
                type="password"
                required
                className="input-field"
                value={form.confirmPassword}
                onChange={(e) => update("confirmPassword", e.target.value)}
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-200 mb-1.5 block">District</label>
              <select
                required
                className="input-field"
                value={form.district}
                onChange={(e) => update("district", e.target.value)}
              >
                <option value="" disabled>
                  Select district
                </option>
                {mockDistricts.map((d) => (
                  <option key={d.id} value={d.name}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-200 mb-1.5 block">Role</label>
              <select className="input-field" value={form.role} onChange={(e) => update("role", e.target.value)}>
                <option value="driver">Driver</option>
                <option value="district_officer">District Officer</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-xs text-slate-200 mb-1.5 block">Phone number (optional)</label>
            <input className="input-field" value={form.phone} onChange={(e) => update("phone", e.target.value)} />
          </div>

          {error && <p className="text-sm text-risk-extreme">{error}</p>}

          <button type="submit" disabled={loading} className="btn-primary w-full">
            <UserPlus className="h-4 w-4" />
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="text-sm text-slate-200 text-center mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-forest-500 hover:text-forest-400 font-medium">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
