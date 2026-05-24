// Role identifiers as they come from the backend
const ADMIN_ROLE = {
  titles: ['Platform Admin'],
  codes: ['platform_admin'],
}

const SUPERVISOR_ROLE = {
  titles: ['Supervisor'],
  codes: ['supervisor'],
}

export function isAdmin(user) {
  if (!user?.roles?.length) return false
  return user.roles.some(
    (r) =>
      ADMIN_ROLE.codes.includes(r.code_name) ||
      ADMIN_ROLE.titles.includes(r.title)
  )
}

export function isSupervisor(user) {
  if (!user?.roles?.length) return false
  return user.roles.some(
    (r) =>
      SUPERVISOR_ROLE.codes.includes(r.code_name) ||
      SUPERVISOR_ROLE.titles.includes(r.title)
  )
}
