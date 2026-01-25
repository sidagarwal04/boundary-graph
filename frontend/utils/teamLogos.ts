// Team logo mapping utility
export interface TeamLogoMapping {
  [key: string]: string
}

export interface TeamColorMapping {
  [key: string]: string
}

export const teamLogoMap: TeamLogoMapping = {
  // Active Teams
  'Chennai Super Kings': '/teams-logos/CSKoutline.avif',
  'Delhi Capitals': '/teams-logos/DCoutline.avif', 
  'Gujarat Titans': '/teams-logos/GToutline.avif',
  'Kolkata Knight Riders': '/teams-logos/KKRoutline.avif',
  'Lucknow Super Giants': '/teams-logos/LSGoutline.avif',
  'Mumbai Indians': '/teams-logos/MIoutline.avif',
  'Punjab Kings': '/teams-logos/PBKSoutline.avif',
  'Royal Challengers Bangalore': '/teams-logos/RCBoutline.avif',
  'Royal Challengers Bengaluru': '/teams-logos/RCBoutline.avif', // Same as Royal Challengers Bangalore
  'Rajasthan Royals': '/teams-logos/RR_Logo.avif',
  'Sunrisers Hyderabad': '/teams-logos/SRHoutline.avif',
  
  // Abbreviated forms
  'CSK': '/teams-logos/CSKoutline.avif',
  'DC': '/teams-logos/DCoutline.avif',
  'DD': '/teams-logos/dd.png', // Delhi Daredevils
  'GT': '/teams-logos/GToutline.avif', 
  'KKR': '/teams-logos/KKRoutline.avif',
  'LSG': '/teams-logos/LSGoutline.avif',
  'MI': '/teams-logos/MIoutline.avif',
  'PBKS': '/teams-logos/PBKSoutline.avif',
  'RCB': '/teams-logos/RCBoutline.avif',
  'RR': '/teams-logos/RR_Logo.avif',
  'SRH': '/teams-logos/SRHoutline.avif',

  // Historical variations
  'Delhi Daredevils': '/teams-logos/dd.png', // Delhi Daredevils original logo
  'Kings XI Punjab': '/teams-logos/PBKSoutline.avif', // Same as Punjab Kings
  
  // Defunct Teams
  'Deccan Chargers': '/teams-logos/HyderabadDeccanChargers.png',
  'Gujarat Lions': '/teams-logos/Gujarat_Lions.png', 
  'Kochi Tuskers Kerala': '/teams-logos/Kochi_Tuskers_Kerala_Logo.svg.png',
  'Pune Warriors India': '/teams-logos/Pune_Warriors_India_IPL_Logo.png',
  'Pune Warriors': '/teams-logos/Pune_Warriors_India_IPL_Logo.png', // Alternative name
  'Rising Pune Supergiant': '/teams-logos/Rising_Pune_Supergiant.png',
  'Rising Pune Supergiants': '/teams-logos/Rising_Pune_Supergiant.png', // Alternative name
}

export const teamColorMap: TeamColorMapping = {
  // Active Teams
  'Chennai Super Kings': '#ffcb03', // Yellow
  'Delhi Capitals': '#b9251c', // Red
  'Gujarat Titans': '#77c7f2', // Light Blue
  'Kolkata Knight Riders': '#ecc542', // Golden Yellow
  'Lucknow Super Giants': '#ffffff', // White
  'Mumbai Indians': '#2d6ab1', // Blue
  'Punjab Kings': '#d71920', // Red
  'Royal Challengers Bangalore': '#2b2a29', // Dark Grey/Black
  'Royal Challengers Bengaluru': '#2b2a29', // Same as RCB
  'Rajasthan Royals': '#eb83b5', // Pink
  'Sunrisers Hyderabad': '#f26522', // Orange
  
  // Abbreviated forms
  'CSK': '#ffcb03',
  'DC': '#b9251c', 
  'DD': '#ffffff', // Delhi Daredevils white background
  'GT': '#77c7f2',
  'KKR': '#ecc542',
  'LSG': '#ffffff',
  'MI': '#2d6ab1',
  'PBKS': '#d71920',
  'RCB': '#2b2a29',
  'RR': '#eb83b5',
  'SRH': '#f26522',

  // Historical variations
  'Delhi Daredevils': '#ffffff', // White background for DD logo
  'Kings XI Punjab': '#d71920',
  
  // Defunct Teams - Grey background to denote defunct status
  'Deccan Chargers': '#9ca3af', // gray-400
  'Gujarat Lions': '#9ca3af', // gray-400
  'Kochi Tuskers Kerala': '#9ca3af', // gray-400  
  'Pune Warriors India': '#9ca3af', // gray-400
  'Pune Warriors': '#9ca3af', // gray-400
  'Rising Pune Supergiant': '#9ca3af', // gray-400
  'Rising Pune Supergiants': '#9ca3af', // gray-400
}

export interface TeamDetailsMapping {
  [key: string]: {
    captain: string
    coach: string 
    owner: string
    venue: string
  }
}

export const teamDetailsMap: TeamDetailsMapping = {
  // Active Teams
  'Chennai Super Kings': {
    captain: 'MS Dhoni',
    coach: 'Stephen Fleming',
    owner: 'Chennai Super Kings Cricket Limited',
    venue: 'M. A. Chidambaram Stadium'
  },
  'Delhi Capitals': {
    captain: 'Axar Patel',
    coach: 'Hemang Badani', 
    owner: 'JSW GMR Cricket Pvt Ltd',
    venue: 'Arun Jaitley Stadium'
  },
  'Gujarat Titans': {
    captain: 'Shubman Gill',
    coach: 'Ashish Nehra',
    owner: 'Irelia Sports India Private Limited',
    venue: 'Narendra Modi Stadium'
  },
  'Kolkata Knight Riders': {
    captain: 'Ajinkya Rahane',
    coach: 'Abhishek Nayar',
    owner: 'Knight Riders Sports Private Limited',
    venue: 'Eden Gardens'
  },
  'Lucknow Super Giants': {
    captain: 'Rishabh Pant',
    coach: 'Justin Langer',
    owner: 'RPSG Sports Private Limited',
    venue: 'BRSABV Ekana Cricket Stadium'
  },
  'Mumbai Indians': {
    captain: 'Hardik Pandya',
    coach: 'Mahela Jayawardene',
    owner: 'Indiawin Sports Pvt. Ltd',
    venue: 'Wankhede Stadium'
  },
  'Punjab Kings': {
    captain: 'Shreyas Iyer',
    coach: 'Ricky Ponting',
    owner: 'K.P.H. Dream Cricket Private Limited',
    venue: 'PCA New Stadium, Mullanpur'
  },
  'Royal Challengers Bangalore': {
    captain: 'Rajat Patidar',
    coach: 'Andy Flower',
    owner: 'Royal Challengers Sports Private Ltd',
    venue: 'M. Chinnaswamy Stadium'
  },
  'Royal Challengers Bengaluru': {
    captain: 'Rajat Patidar',
    coach: 'Andy Flower',
    owner: 'Royal Challengers Sports Private Ltd',
    venue: 'M. Chinnaswamy Stadium'
  },
  'Rajasthan Royals': {
    captain: 'Sanju Samson',
    coach: 'Kumar Sangakkara',
    owner: 'Royal Multisport Private Limited',
    venue: 'Sawai Mansingh Stadium'
  },
  'Sunrisers Hyderabad': {
    captain: 'Pat Cummins',
    coach: 'Daniel Vettori',
    owner: 'Sun TV Network Limited',
    venue: 'Rajiv Gandhi Intl. Cricket Stadium'
  },

  // Abbreviated forms
  'CSK': {
    captain: 'MS Dhoni',
    coach: 'Stephen Fleming',
    owner: 'Chennai Super Kings Cricket Limited',
    venue: 'M. A. Chidambaram Stadium'
  },
  'DC': {
    captain: 'Axar Patel',
    coach: 'Hemang Badani',
    owner: 'JSW GMR Cricket Pvt Ltd', 
    venue: 'Arun Jaitley Stadium'
  },
  'GT': {
    captain: 'Shubman Gill',
    coach: 'Ashish Nehra',
    owner: 'Irelia Sports India Private Limited',
    venue: 'Narendra Modi Stadium'
  },
  'KKR': {
    captain: 'Ajinkya Rahane',
    coach: 'Abhishek Nayar',
    owner: 'Knight Riders Sports Private Limited',
    venue: 'Eden Gardens'
  },
  'LSG': {
    captain: 'Rishabh Pant',
    coach: 'Justin Langer',
    owner: 'RPSG Sports Private Limited',
    venue: 'BRSABV Ekana Cricket Stadium'
  },
  'MI': {
    captain: 'Hardik Pandya',
    coach: 'Mahela Jayawardene',
    owner: 'Indiawin Sports Pvt. Ltd',
    venue: 'Wankhede Stadium'
  },
  'PBKS': {
    captain: 'Shreyas Iyer',
    coach: 'Ricky Ponting',
    owner: 'K.P.H. Dream Cricket Private Limited',
    venue: 'PCA New Stadium, Mullanpur'
  },
  'RCB': {
    captain: 'Rajat Patidar',
    coach: 'Andy Flower',
    owner: 'Royal Challengers Sports Private Ltd',
    venue: 'M. Chinnaswamy Stadium'
  },
  'RR': {
    captain: 'Sanju Samson',
    coach: 'Kumar Sangakkara',
    owner: 'Royal Multisport Private Limited',
    venue: 'Sawai Mansingh Stadium'
  },
  'SRH': {
    captain: 'Pat Cummins',
    coach: 'Daniel Vettori',
    owner: 'Sun TV Network Limited',
    venue: 'Rajiv Gandhi Intl. Cricket Stadium'
  }
}

/**
 * Get team color for a given team name
 * @param teamName - Team name to get color for
 * @returns Color hex code or default color if not found
 */
export function getTeamColor(teamName: string): string {
  if (!teamName) return '#64748B' // Default slate-500 color
  
  // Direct match
  if (teamColorMap[teamName]) {
    return teamColorMap[teamName]
  }
  
  // Try partial matches for teams that might have slight variations
  const colorPartialMatches: Array<[string, string]> = [
    ['Chennai', '#ffcb03'],
    ['Delhi Daredevils', '#ffffff'], // White background for DD
    ['Delhi', '#b9251c'], // Delhi Capitals (fallback)
    ['Gujarat Titans', '#77c7f2'], // Only Gujarat Titans
    ['Gujarat Lions', '#9ca3af'], // Defunct team - grey
    ['Kolkata', '#ecc542'],
    ['Lucknow', '#ffffff'],
    ['Mumbai', '#2d6ab1'],
    ['Punjab', '#d71920'],
    ['Royal Challengers', '#2b2a29'],
    ['Rajasthan', '#eb83b5'],
    ['Sunrisers', '#f26522'],
    ['Deccan', '#9ca3af'], // Defunct team - grey
    ['Kochi', '#9ca3af'], // Defunct team - grey
    ['Pune Warriors', '#9ca3af'], // Defunct team - grey
    ['Rising Pune', '#9ca3af'], // Defunct team - grey
  ]
  
  for (const [keyword, color] of colorPartialMatches) {
    if (teamName.includes(keyword)) {
      return color
    }
  }
  
  return '#64748B' // Default slate-500 color
}

/**
 * Get team logo URL for a given team name
 * @param teamName - Team name to get logo for
 * @returns Logo URL or null if not found
 */
export function getTeamLogo(teamName: string): string | null {
  if (!teamName) return null
  
  // Direct match
  if (teamLogoMap[teamName]) {
    return teamLogoMap[teamName]
  }
  
  // Try to match by removing common variations
  const normalizedName = teamName.trim()
  
  // Try partial matches for teams that might have slight variations
  const partialMatches: Array<[string, string]> = [
    ['Chennai', '/teams-logos/CSKoutline.avif'],
    ['Delhi Daredevils', '/teams-logos/dd.png'], // More specific match first
    ['Delhi', '/teams-logos/DCoutline.avif'], // Delhi Capitals (fallback)
    ['Gujarat Titans', '/teams-logos/GToutline.avif'], // Only Gujarat Titans, not Gujarat Lions
    ['Gujarat Lions', '/teams-logos/Gujarat_Lions.png'], // Defunct team
    ['Kolkata', '/teams-logos/KKRoutline.avif'],
    ['Lucknow', '/teams-logos/LSGoutline.avif'],
    ['Mumbai', '/teams-logos/MIoutline.avif'],
    ['Punjab', '/teams-logos/PBKSoutline.avif'],
    ['Royal Challengers', '/teams-logos/RCBoutline.avif'],
    ['Rajasthan', '/teams-logos/RR_Logo.avif'],
    ['Sunrisers', '/teams-logos/SRHoutline.avif'],
    ['Deccan', '/teams-logos/HyderabadDeccanChargers.png'],
    ['Kochi', '/teams-logos/Kochi_Tuskers_Kerala_Logo.svg.png'],
    ['Pune Warriors', '/teams-logos/Pune_Warriors_India_IPL_Logo.png'],
    ['Rising Pune', '/teams-logos/Rising_Pune_Supergiant.png'],
  ]
  
  for (const [keyword, logo] of partialMatches) {
    if (normalizedName.includes(keyword)) {
      return logo
    }
  }
  
  return null
}

/**
 * Get team abbreviation from full name
 * @param teamName - Full team name
 * @returns Team abbreviation or original name if no abbreviation found
 */
export function getTeamAbbreviation(teamName: string): string {
  const abbreviations: { [key: string]: string } = {
    'Chennai Super Kings': 'CSK',
    'Delhi Capitals': 'DC',
    'Delhi Daredevils': 'DC',
    'Gujarat Titans': 'GT', 
    'Kolkata Knight Riders': 'KKR',
    'Lucknow Super Giants': 'LSG',
    'Mumbai Indians': 'MI',
    'Punjab Kings': 'PBKS',
    'Kings XI Punjab': 'PBKS',
    'Royal Challengers Bangalore': 'RCB',
    'Royal Challengers Bengaluru': 'RCB',
    'Rajasthan Royals': 'RR',
    'Sunrisers Hyderabad': 'SRH',
    // Defunct Teams
    'Deccan Chargers': 'DC',
    'Gujarat Lions': 'GL',
    'Kochi Tuskers Kerala': 'KTK',
    'Pune Warriors India': 'PWI',
    'Pune Warriors': 'PWI',
    'Rising Pune Supergiant': 'RPS',
    'Rising Pune Supergiants': 'RPS',
  }
  
  return abbreviations[teamName] || teamName
}

/**
 * Get team details (captain, coach, owner, venue) for a given team name
 * @param teamName - Team name to get details for
 * @returns Team details or null if not found
 */
export function getTeamDetails(teamName: string): TeamDetailsMapping[string] | null {
  if (!teamName) return null
  
  // Direct match
  if (teamDetailsMap[teamName]) {
    return teamDetailsMap[teamName]
  }
  
  // Try partial matches for teams that might have slight variations
  const detailsPartialMatches: Array<[string, TeamDetailsMapping[string]]> = [
    ['Chennai', teamDetailsMap['Chennai Super Kings']],
    ['Delhi', teamDetailsMap['Delhi Capitals']],
    ['Gujarat Titans', teamDetailsMap['Gujarat Titans']], // Only Gujarat Titans
    ['Kolkata', teamDetailsMap['Kolkata Knight Riders']],
    ['Lucknow', teamDetailsMap['Lucknow Super Giants']],
    ['Mumbai', teamDetailsMap['Mumbai Indians']],
    ['Punjab', teamDetailsMap['Punjab Kings']],
    ['Royal Challengers', teamDetailsMap['Royal Challengers Bangalore']],
    ['Rajasthan', teamDetailsMap['Rajasthan Royals']],
    ['Sunrisers', teamDetailsMap['Sunrisers Hyderabad']],
  ]
  
  for (const [keyword, details] of detailsPartialMatches) {
    if (teamName.includes(keyword)) {
      return details
    }
  }
  
  return null
}

/**
 * Check if a team is defunct (no longer active in IPL)
 * @param teamName - Team name to check
 * @returns true if team is defunct, false otherwise
 */
export function isDefunctTeam(teamName: string): boolean {
  if (!teamName) return false
  
  const defunctTeams = [
    'Deccan Chargers',
    'Gujarat Lions',
    'Kochi Tuskers Kerala', 
    'Pune Warriors India',
    'Pune Warriors',
    'Rising Pune Supergiant',
    'Rising Pune Supergiants'
  ]
  
  // Direct match
  if (defunctTeams.includes(teamName)) {
    return true
  }
  
  // Try partial matches for teams that might have slight variations
  const defunctKeywords = ['Gujarat Lions', 'Deccan', 'Kochi', 'Pune Warriors', 'Rising Pune']
  for (const keyword of defunctKeywords) {
    if (teamName.includes(keyword)) {
      return true
    }
  }
  
  return false
}