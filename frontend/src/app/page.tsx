import { redirect } from "next/navigation";

/**
 * [ES] La página raíz redirige al dashboard. / [EN] Root page redirects to the dashboard.
 */
export default function RootPage() {
  redirect("/dashboard");
}
