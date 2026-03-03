/**
 * Composable for checking backend health and waiting for service to be active
 * Handles Render cold starts by polling the backend until it's ready
 */

import { ref } from 'vue'

interface HealthResponse {
  message: string
  status: string
}

export const useBackendHealth = () => {
  const config = useRuntimeConfig()
  const isBackendActive = ref(false)
  const isCheckingHealth = ref(true)
  const error = ref<string | null>(null)
  
  const MAX_ATTEMPTS = 60 // 60 attempts with 2s interval = 2 minutes max wait
  const POLL_INTERVAL = 2000 // 2 seconds
  
  /**
   * Check if backend is active by hitting the root endpoint
   */
  const checkBackendHealth = async (): Promise<boolean> => {
    try {
      const apiBase = config.public.apiBase as string
      const response = await $fetch<HealthResponse>(`${apiBase}/`)
      
      if (
        response.message === "IPL Cricket Dashboard API is running" &&
        response.status === "active"
      ) {
        return true
      }
    } catch (err) {
      // Backend not ready yet
      console.log('⏳ Backend not ready yet, retrying...')
    }
    
    return false
  }
  
  /**
   * Poll the backend until it's active or max attempts reached
   */
  const waitForBackendToBeActive = async () => {
    let attempts = 0
    
    while (attempts < MAX_ATTEMPTS) {
      const isActive = await checkBackendHealth()
      
      if (isActive) {
        console.log('✅ Backend is now active!')
        isBackendActive.value = true
        isCheckingHealth.value = false
        return true
      }
      
      attempts++
      console.log(`⏳ Waiting for backend... (attempt ${attempts}/${MAX_ATTEMPTS})`)
      
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL))
    }
    
    // Max attempts reached
    error.value = 'Backend service is taking longer than expected. Please refresh the page.'
    isCheckingHealth.value = false
    return false
  }
  
  /**
   * Initialize health check on component mount
   */
  const initHealthCheck = async () => {
    isCheckingHealth.value = true
    isBackendActive.value = false
    
    // First, try immediately
    const isActive = await checkBackendHealth()
    
    if (isActive) {
      isBackendActive.value = true
      isCheckingHealth.value = false
      console.log('✅ Backend is active')
    } else {
      // Backend not ready, start polling
      console.log('⏳ Backend not ready, starting polling...')
      await waitForBackendToBeActive()
    }
  }
  
  return {
    isBackendActive,
    isCheckingHealth,
    error,
    initHealthCheck,
    checkBackendHealth,
    waitForBackendToBeActive
  }
}
