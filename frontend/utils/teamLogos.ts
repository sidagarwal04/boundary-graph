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
  'GT': '/teams-logos/GToutline.avif', 
  'KKR': '/teams-logos/KKRoutline.avif',
  'LSG': '/teams-logos/LSGoutline.avif',
  'MI': '/teams-logos/MIoutline.avif',
  'PBKS': '/teams-logos/PBKSoutline.avif',
  'RCB': '/teams-logos/RCBoutline.avif',
  'RR': '/teams-logos/RR_Logo.avif',
  'SRH': '/teams-logos/SRHoutline.avif',

  // Historical variations
  'Delhi Daredevils': '/teams-logos/DCoutline.avif', // Same as Delhi Capitals
  'Kings XI Punjab': '/teams-logos/PBKSoutline.avif', // Same as Punjab Kings
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
  'GT': '#77c7f2',
  'KKR': '#ecc542',
  'LSG': '#ffffff',
  'MI': '#2d6ab1',
  'PBKS': '#d71920',
  'RCB': '#2b2a29',
  'RR': '#eb83b5',
  'SRH': '#f26522',

  // Historical variations
  'Delhi Daredevils': '#b9251c',
  'Kings XI Punjab': '#d71920',
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
    ['Delhi', '#b9251c'],
    ['Gujarat Titans', '#77c7f2'], // Only Gujarat Titans
    ['Kolkata', '#ecc542'],
    ['Lucknow', '#ffffff'],
    ['Mumbai', '#2d6ab1'],
    ['Punjab', '#d71920'],
    ['Royal Challengers', '#2b2a29'],
    ['Rajasthan', '#eb83b5'],
    ['Sunrisers', '#f26522'],
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
    ['Delhi', '/teams-logos/DCoutline.avif'],
    ['Gujarat Titans', '/teams-logos/GToutline.avif'], // Only Gujarat Titans, not Gujarat Lions
    ['Kolkata', '/teams-logos/KKRoutline.avif'],
    ['Lucknow', '/teams-logos/LSGoutline.avif'],
    ['Mumbai', '/teams-logos/MIoutline.avif'],
    ['Punjab', '/teams-logos/PBKSoutline.avif'],
    ['Royal Challengers', '/teams-logos/RCBoutline.avif'],
    ['Rajasthan', '/teams-logos/RR_Logo.avif'],
    ['Sunrisers', '/teams-logos/SRHoutline.avif'],
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