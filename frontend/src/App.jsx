
// minimal users dashboard with search and list functionality

import React, { useEffect, useState } from "react"

// api base url - reads from .env set at build time, or in prod falls back to /api
const BASE = import.meta.env.VITE_API_BASE ?? "/api"

/**
 * fetch json from an endpoint with error handling.
 * 
 * params:
 *   url: endpoint to fetch from
 * returns:
 *   parsed json response
 * throws:
 *   Error if request fails
 */
async function fetchJson(url) {
  const res = await fetch(url, { headers: { accept: "application/json" } })
  if (!res.ok) {
    const text = await res.text().catch(() => "")
    throw new Error(`request failed (${res.status}): ${text || res.statusText}`)
  }
  return res.json()
}

/**
 * format iso date string to yyyy-mm-dd.
 * 
 * params:
 *   iso: iso date string
 * returns:
 *   formatted date or original string if invalid
 */
function prettyDate(iso) {
  if (!iso) return ""
  const d = new Date(iso)
  return isNaN(d.getTime()) ? String(iso) : d.toISOString().slice(0, 10)
  //checks if validand returns a formatted date, else return the original string
}

/**
 * single table row component.
 * 
 * params:
 *   user: user object with all fields
 */
function Row({ user }) {
  const fullName = [user?.first_name, user?.last_name].filter(Boolean).join(" ")
  
  // metadata col that shows the rest of the fields
  const metadata = Object.entries(user || {})  // convert a user into k/v array
    .map(([k, v]) => `${k}: ${v ?? ""}`)
    .join(" | ")
  
  return (
    <tr className="hover:bg-slate-50">
      <td className="px-4 py-3 font-mono text-xs">{user?.id}</td>
      <td className="px-4 py-3">{fullName || "—"}</td>
      <td className="px-4 py-3">{user?.department || "—"}</td>
      <td className="px-4 py-3">{user?.job_title || "—"}</td>
      <td className="px-4 py-3">{prettyDate(user?.date_of_birth)}</td>
      <td className="px-4 py-3">{prettyDate(user?.created_at)}</td>
      <td className="px-4 py-3 text-xs text-slate-600">{metadata}</td>
    </tr>
  )
}

/**
 * users table component.
 * 
 * params:
 *   users: array of user objects
 */
function Table({ users }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-100 text-slate-700">
          <tr>
            <th className="px-4 py-2 text-left">id</th>
            <th className="px-4 py-2 text-left">name</th>
            <th className="px-4 py-2 text-left">department</th>
            <th className="px-4 py-2 text-left">job title</th>
            <th className="px-4 py-2 text-left">dob</th>
            <th className="px-4 py-2 text-left">created</th>
            <th className="px-4 py-2 text-left">metadata</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {users.map((u) => (
            <Row key={u.id} user={u} /> 
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function App() {
  const [query, setQuery] = useState("") 
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  // fetch all users on mount
  useEffect(() => {
    void fetchAll()
  }, [])

  /**
   * fetch all users from the api.
   */
  async function fetchAll() {
    setLoading(true)
    setError("")   
    try {
      const data = await fetchJson(`${BASE}/users`)
      // makes an api call
      const arr = data?.users || data?.data || (Array.isArray(data) ? data : [])
      setUsers(arr)
    } catch (e) {
      setError(e.message || String(e))
      setUsers([])
    } finally {
      setLoading(false)
    }
  }

  /**
   * search for a single user by id.
   */
  async function searchById() {
    const id = String(query || "").trim() 
    if (!id) return
    
    setLoading(true)
    setError("")
    try {
      const data = await fetchJson(`${BASE}/users/${encodeURIComponent(id)}`)
      const user = data?.user || data
      setUsers(user ? [user] : [])
      if (!user) setError("no result")
    } catch (e) {
      setUsers([])
      setError(e.message || "not found")
    } finally {
      setLoading(false)
    }
  }

  /**
   * clear search input and results.
   */
  function clearResults() {
    setQuery("")
    setUsers([])
    setError("")
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-4 flex items-center gap-3">
          <div className="h-4 w-4 rounded-lg bg-blue-600" />
          <h1 className="text-lg font-semibold">user list</h1>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 space-y-8">
        {/* search controls */}
        <section className="rounded-xl border border-slate-200 bg-white p-4">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">search</h2>
          <div className="flex flex-wrap items-center gap-3">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="enter user id (e.g., 1)"
              className="w-48 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={searchById}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
            >
              search
            </button>
            <button
              onClick={clearResults}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
            >
              clear users
            </button>
            <button
              onClick={fetchAll}
              className="rounded-lg border border-blue-600 text-blue-600 px-4 py-2 text-sm hover:bg-blue-50"
            >
              fetch all
            </button>
            <div className="ml-auto text-xs text-slate-500">
              {users.length ? `${users.length} result(s)` : ""}
            </div>
          </div>
          
          {/* status messages */}
          <div className="mt-3 h-5">
            {loading && <span className="text-xs text-slate-500">loading</span>}
            {!loading && error && (
              <span className="text-xs text-red-600">error: {error}</span>
            )}
          </div>
        </section>

        {/* users table or empty state */}
        <section className="space-y-3">
          <h2 className="text-sm font-semibold text-slate-700">users</h2>
          {users.length === 0 && !loading ? (
            <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">
              no data match — try "fetch all" or search by id
            </div>
          ) : (
            <Table users={users} />
          )}
        </section>
      </main>

      <footer className="py-6 text-center text-xs text-slate-400">
        
      </footer>
    </div>
  )
}
