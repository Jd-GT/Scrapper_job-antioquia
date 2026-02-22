"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Briefcase, 
  BarChart3, 
  Download, 
  TrendingUp
} from "lucide-react";
import { clsx } from "clsx";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/ofertas", label: "Ofertas", icon: Briefcase },
  { href: "/analisis", label: "Análisis", icon: BarChart3 },
  { href: "/exportar", label: "Exportar", icon: Download },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900 border-r border-teal-900/40 flex flex-col z-50">
      <div className="p-6 border-b border-teal-900/40">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center shadow-lg">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-display font-bold text-slate-100">Empleos Antioquia</h1>
            <p className="text-xs text-slate-500">Market Analytics</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1.5">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
                isActive 
                  ? "bg-teal-500/15 text-teal-300 border border-teal-500/30" 
                  : "text-slate-400 hover:bg-teal-500/10 hover:text-teal-200 border border-transparent"
              )}
            >
              <Icon className={clsx(
                "w-5 h-5 transition-colors",
                isActive ? "text-teal-400" : "text-slate-500 group-hover:text-teal-300"
              )} />
              <span className="font-medium">{item.label}</span>
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-teal-400 shadow-lg" />
              )}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-teal-900/40">
        <div className="px-4 py-3 bg-slate-800/60 rounded-xl border border-teal-900/30">
          <p className="text-xs text-slate-500">Última actualización</p>
          <p className="text-sm font-mono text-teal-400">22 Feb 2026</p>
        </div>
      </div>
    </aside>
  );
}
