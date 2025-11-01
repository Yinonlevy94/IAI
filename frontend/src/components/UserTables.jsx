// UserTables.jsx
// simple table component (not currently used in App.jsx)

/**
 * basic users table component.
 * 
 * params:
 *   rows: array of user objects with id, name, email
 
export default function UsersTable({ rows = [] }) {
  return (
    <div className="w-full overflow-x-auto bg-white border border-borderClr rounded-xl shadow-soft">
      <table className="w-full border-collapse min-w-table">
        <thead className="bg-primary text-white">
          <tr>
            <th className="p-3 text-left font-bold">id</th>
            <th className="p-3 text-left font-bold">name</th>
            <th className="p-3 text-left font-bold">email</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.id} className="odd:bg-white even:bg-[#f9fbff] hover:bg-[#eef3ff]">
              <td className="p-3 border-b border-borderClr">{r.id}</td>
              <td className="p-3 border-b border-borderClr">{r.name}</td>
              <td className="p-3 border-b border-borderClr">{r.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
*/
