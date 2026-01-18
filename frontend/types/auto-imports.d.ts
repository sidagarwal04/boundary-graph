declare global {
  const useRuntimeConfig: typeof import('#app').useRuntimeConfig
  const useRoute: typeof import('vue-router').useRoute
  const useRouter: typeof import('vue-router').useRouter
  const navigateTo: typeof import('#app').navigateTo
  const $fetch: typeof import('ofetch').$fetch
}

export {}
