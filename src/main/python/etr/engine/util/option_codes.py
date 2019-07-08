"""
Vehicle option codes and their meanings

The codes were obtained from https://tesla-api.timdorr.com/vehicle/optioncodes
"""


def translate_codes(option_codes):
    """
    Translate a set of option codes into a tupple list

    :param option_codes: string containing the option codes separated by comma
    :return: tupple list containing the option codes and their meanings
    """
    code_list = option_codes.split(',')
    result = []
    for code in code_list:
        if code in CODES:
            result.append((code, CODES[code]))
        else:
            result.append((code, '?'))
    return result


VALID_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,'


SEPARATOR_CHARS = ','


CODES = {
    'MDLS': 'Model S',
    'MS03': 'Model S',
    'MS04': 'Model S',
    'MDLX': 'Model X',
    'MDL3': 'Model 3',
    'RENA': 'Region: North America',
    'RENC': 'Region: Canada',
    'REEU': 'Region: Europe',
    'AD02': 'NEMA 14-50',
    'AD04': 'European 3-Phase',
    'AD05': 'European 3-Phase, IT',
    'AD06': 'Schuko (1 phase, 230V 13A)',
    'AD07': 'Red IEC309 (3 phase, 400V 16A)',
    'AD15': '?',
    'ADPX2': 'Type 2 Public Charging Connector',
    'ADX8': 'Blue IEC309 (1 phase, 230V 32A)',
    'AF00': 'No HEPA Filter',
    'AF02': 'HEPA Filter',
    'AH00': 'No Accessory Hitch',
    'APE1': 'Enhanced Autopilot',
    'APF0': 'Autopilot Firmware 2.0 Base',
    'APF1': 'Autopilot Firmware 2.0 Enhanced',
    'APF2': 'Full Self-Driving Capability',
    'APH0': 'Autopilot 2.0 Hardware',
    'APH2': 'Autopilot 2.0 Hardware',
    'APH3': 'Autopilot 2.5 Hardware',
    'APH4': 'Autopilot 3.0 Hardware',
    'APPA': 'Autopilot 1.0 Hardware',
    'APPB': 'Enhanced Autopilot',
    'AU00': 'No Audio Package',
    'AU01': 'Ultra High Fidelity Sound',
    'BC0B': 'Tesla Black Brake Calipers',
    'BC0R': 'Tesla Red Brake Calipers',
    'BCMB': 'Black Brake Calipers',
    'BP00': 'No Ludicrous',
    'BP01': 'Ludicrous Speed Upgrade',
    'BR00': 'No Battery Firmware Limit',
    'BR03': 'Battery Firmware Limit (60kWh)',
    'BR05': 'Battery Firmware Limit (75kWh)',
    'BS00': 'General Production Flag',
    'BS01': 'Special Production Flag',
    'BT37': '75 kWh (Model 3)',
    'BT40': '40 kWh',
    'BT60': '60 kWh',
    'BT70': '70 kWh',
    'BT85': '85 kWh',
    'BTX4': '90 kWh',
    'BTX5': '75 kWh',
    'BTX6': '100 kWh',
    'BTX7': '75 kWh',
    'BTX8': '85 kWh',
    'CC04': 'Seven Seat Interior',
    'CDM0': 'No CHAdeMO Charging Adaptor',
    'CH00': 'Standard Charger (40 Amp)',
    'CH01': 'Dual Chargers (80 Amp)',
    'CH04': '72 Amp Charger (Model S/X)',
    'CH05': '48 Amp Charger (Model S/X)',
    'CH07': '48 Amp Charger (Model 3)',
    'COL0': 'Signature',
    'COL1': 'Solid',
    'COL2': 'Metallic',
    'COL3': 'Tesla Multi-Coat',
    'COUS': 'Country: United States',
    'CONL': 'Country: Netherlands',
    'CW00': 'No Cold Weather Package',
    'CW02': 'Subzero Weather Package',
    'DA00': 'No Autopilot',
    'DA01': 'Active Safety (ACC,LDW,SA)',
    'DA02': 'Autopilot Convenience Features',
    'DCF0': 'Autopilot Convenience Features (DCF0)',
    'DRLH': 'Left Hand Drive',
    'DRRH': 'Right Hand Drive',
    'DSH5': 'PUR Dash Pad',
    'DSH7': 'Alcantara Dashboard Accents',
    'DSHG': 'PUR Dash Pad',
    'DU00': 'Drive Unit - IR',
    'DU01': 'Drive Unit - Infineon',
    'DV2W': 'Rear-Wheel Drive',
    'DV4W': 'All-Wheel Drive',
    'FG00': 'No Exterior Lighting Package',
    'FG01': 'Exterior Lighting Package',
    'FG02': 'Exterior Lighting Package',
    'FMP6': '?',
    'FR01': 'Base Front Row',
    'FR03': '?',
    'FR04': '?',
    'HC00': 'No Home Charging installation',
    'HC01': 'Home Charging Installation',
    'HP00': 'No HPWC Ordered',
    'HP01': 'HPWC Ordered',
    'ID3W': '(Model 3) Wood Decor',
    'IDBA': 'Dark Ash Wood Decor',
    'IDBO': 'Figured Ash Wood Decor',
    'IDCF': 'Carbon Fiber Decor',
    'IDOM': 'Matte Obeche Wood Decor',
    'IDOG': 'Gloss Obeche Wood Decor',
    'IDLW': 'Lacewood Decor',
    'IDPB': 'Piano Black Decor',
    'IN3BB': 'All Black Partial Premium Interior',
    'IN3PB': 'All Black Premium Interior',
    'INBBW': 'White',
    'INBFP': 'Classic Black',
    'INBPP': 'Black',
    'INBTB': 'Multi-Pattern Black',
    'INFBP': 'Black Premium',
    'INLPC': 'Cream',
    'INLPP': 'Black / Light Headliner',
    'INWPT': 'Tan Interior',
    'IVBPP': 'All Black Interior',
    'IVBSW': 'Ultra White Interior',
    'IVBTB': 'All Black Interior',
    'IVLPC': 'Vegan Cream',
    'IX00': 'No Extended Nappa Leather Trim',
    'IX01': 'Extended Nappa Leather Trim',
    'LLP1': '?',
    'LLP2': '?',
    'LP01': 'Premium Interior Lighting',
    'LT00': 'Vegan interior',
    'LT01': 'Standard interior',
    'LT1B': '?',
    'LT3W': '?',
    'LT4B': '?',
    'LT4C': '?',
    'LT4W': '?',
    'LT5C': '?',
    'LT5P': '?',
    'LT6P': '?',
    'ME02': 'Memory Seats',
    'MI00': '2015 Production Refresh',
    'MI01': '2016 Production Refresh',
    'MI02': '2017 Production Refresh',
    'MI03': '???? Production Refresh',
    'MT301': 'Standard Range Plus Rear-Wheel Drive',
    'MT305': 'Mid Range Rear-Wheel Drive',
    'OSSB': '?',
    'PA00': 'No Paint Armor',
    'PBCW': 'Catalina White',
    'PBSB': 'Sierra Black',
    'PBT8': 'Performance 85kWh',
    'PF00': 'No Performance Legacy Package',
    'PF01': 'Performance Legacy Package',
    'PI00': 'No Premium Interior',
    'PI01': 'Premium Upgrades Package',
    'PK00': 'LEGACY No Parking Sensors',
    'PMAB': 'Anza Brown Metallic',
    'PMBL': 'Obsidian Black Multi-Coat',
    'PMMB': 'Monterey Blue Metallic',
    'PMMR': 'Multi-Coat Red',
    'PMNG': 'Midnight Silver Metallic',
    'PMSG': 'Sequoia Green Metallic',
    'PMSS': 'San Simeon Silver Metallic',
    'PMTG': 'Dolphin Grey Metallic',
    'PPMR': 'Muir Red Multi-Coat',
    'PPSB': 'Deep Blue Metallic',
    'PPSR': 'Signature Red',
    'PPSW': 'Shasta Pearl White Multi-Coat',
    'PPTI': 'Titanium Metallic',
    'PRM30': 'Partial Premium Interior',
    'PRM31': 'Premium Interior',
    'PS00': 'No Parcel Shelf',
    'PS01': 'Parcel Shelf',
    'PX00': 'No Performance Plus Package',
    'PX01': 'Performance Plus',
    'PX6D': 'Zero to 60 in 2.5 sec',
    'P85D': 'P85D',
    'QNET': 'Tan NextGen',
    'QPMP': 'Black seats',
    'QTBW': 'White Premium Seats',
    'QTFP': 'Black Premium Seats',
    'QTPC': 'Cream Premium Seats',
    'QTPP': 'Black Premium Seats',
    'QTPT': 'Tan Premium Seats',
    'QTTB': 'Multi-Pattern Black Seats',
    'QVBM': 'Multi-Pattern Black Seats',
    'QVPC': 'Vegan Cream Seats',
    'QVPP': 'Vegan Cream Seats',
    'QVSW': 'White Tesla Seats',
    'RCX0': 'No Rear Console',
    'RF3G': 'Model 3 Glass Roof',
    'RFBK': 'Black Roof',
    'RFBC': 'Body Color Roof',
    'RFFG': 'Glass Roof',
    'RFP0': 'All Glass Panoramic Roof',
    'RFP2': 'Sunroof',
    'RFPX': 'Model X Roof',
    'S02P': '?',
    'S31B': '?',
    'S32C': '?',
    'S32P': '?',
    'S32W': '?',
    'SC00': 'No Supercharging',
    'SC01': 'Supercharging Enabled',
    'SC04': 'Pay Per Use Supercharging',
    'SC05': 'Free Supercharging',
    'SP00': 'No Security Package',
    'SR01': 'Standard 2nd row',
    'SR06': 'Seven Seat Interior',
    'SR07': 'Standard 2nd row',
    'ST00': 'Non-leather Steering Wheel',
    'ST01': 'Non-heated Leather Steering Wheel',
    'SU00': 'Standard Suspension',
    'SU01': 'Smart Air Suspension',
    'TIC4': 'All-Season Tires',
    'TM00': 'General Production Trim',
    'TM02': 'General Production Signature Trim',
    'TM0A': 'ALPHA PRE-PRODUCTION NON-SALEABLE',
    'TM0B': 'BETA PRE-PRODUCTION NON-SALEABLE',
    'TM0C': 'PRE-PRODUCTION SALEABLE',
    'TP01': 'Tech Package - No Autopilot',
    'TP02': 'Tech Package with Autopilot',
    'TP03': 'Tech Package with Enhanced Autopilot',
    'TR00': 'No Third Row Seat',
    'TR01': 'Third Row Seating',
    'TRA1': 'Third Row HVAC',
    'TW01': 'Towing Package',
    'UM01': 'Universal Mobile Charger - US Port (Single)',
    'UTAB': 'Black Alcantara Headliner',
    'UTAW': 'Light Headliner',
    'UTPB': 'Dark Headliner',
    'UTSB': 'Dark Headliner',
    'W38B': '18" Aero Wheels',
    'W39B': '19" Sport Wheels',
    'WT20': '20" Silver Slipstream Wheels',
    'WTAS': '19" Silver Slipstream Wheels',
    'WTDS': '19" Grey Slipstream Wheels',
    'WTSG': '21" Turbine Wheels',
    'WTSP': '21" Turbine Wheels',
    'WTSS': '21" Turbine Wheels',
    'WTTB': '19" Cyclone Wheels',
    'WTW4': '19" Winter Tire Set',
    'WTW5': '21" Winter Tire Set',
    'WTX1': '19" Michelin Primacy Tire Upgrade',
    'WXW4': 'No 19" Winter Tire Set',
    'WXW5': 'No 21" Winter Tire Set',
    'X001': 'Override: Power Liftgate',
    'X003': 'Maps & Navigation',
    'X004': 'Override: No Navigation',
    'X007': 'Daytime running lights',
    'X010': 'Base Mirrors',
    'X011': 'Override: Homelink',
    'X012': 'Override: No Homelink',
    'X013': 'Override: Satellite Radio',
    'X014': 'Override: No Satellite Radio',
    'X019': 'Carbon Fiber Spoiler',
    'X020': 'No Performance Exterior',
    'X021': 'No Spoiler',
    'X024': 'Performance Package',
    'X025': 'No Performance Package',
    'X027': 'Lighted Door Handles',
    'X028': 'Battery Badge',
    'X029': 'Remove Battery Badge',
    'X030': 'Override: No Passive Entry Pkg',
    'X031': 'Keyless Entry',
    'X037': 'Powerfolding Mirrors',
    'X039': 'DAB Radio',
    'X040': 'No DAB Radio',
    'X043': 'No Phone Dock Kit',
    'X044': 'Phone Dock Kit',
    'YF00': 'No Yacht Floor',
    'YF01': 'Matching Yacht Floor',
    'YFCC': '?',
    'YFFC': 'Integrated Center Console'
}
