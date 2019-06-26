from  datetime import date

MONTHS = [(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), 
        (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), 
        (10, 'Oct'), (11, 'Nov'), (12, 'Dec')]

THIS_YEAR = date.today().year

TEST_SAMPLES = ['SIB603A6', 'ADM1852A2', 'SIB603A3', 'SER305A1', 'AND51A3', 'BRA1907A5', 'SIB552A11', 'SIB603A9', 'SIB257A27', 'SIB552A15', 'SIB611A3', 'SIB552A16', 'SIB256A3', 'SIB601A5', 'SIB553A24', 'SIB404A15', 'SIB404A13', 'SIB663A2', 'SIB701A1', 'SIB552A18', 'SIB257A26', 'SER303A1', 'SIB553A27', 'SIB257A23', 'SIB607A1', 'SIB603A2', 'SIB404A14', 'SIB403A27', 'SIB603A12', 'SIB603A14', 'SIB601A11', 'SER305A2', 'SIB663A4', 'ADM1852A1', 'SIB552A12', 'SIB552A13', 'SIB552A10', 'SIB553A19', 'SIB553A10', 'SIB553A15', 'SIB603A8', 'SIB603A4', 'SIB553A17', 'SIB603A16', 'SIB652A1', 'SIB552A3', 'SIB552A4', 'SIB601A7', 'SIB553A28', 'SIB552A2', 'SIB603A18', 'BRA1907A1', 'SIB404A17', 'SIB404A16', 'SIB553A3', 'SIB256A1', 'BIL1393A1', 'SIB601A1', 'SIB603A10', 'SER305A5', 'SIB603A5', 'SER305A4', 'ADM1851A4', 'SER305A6', 'SER307A8', 'BRA1907A4', 'BRA1907A3', 'SIB601A4', 'SER307A7', 'BRA1907A2', 'SIB257A25', 'SIB603A13', 'SIB601A12', 'SIB601A14', 'SER305A7', 'SIB552A17', 'SIB256A2', 'SIB553A14', 'SIB601A2', 'SIB553A12', 'SIB603A20', 'SIB553A13', 'SIB553A9', 'SIB404A19', 'ADM1852A3', 'SIB606A2', 'SIB404A18', 'SIB552A5', 'SIB603A1', 'SIB552A6', 'SER305A3', 'SIB552A8', 'SIB351A22', 'SER307A4', 'SIB603A15', 'SER305A8', 'SIB603A19', 'SIB553A7', 'SIB611A1', 'SIB553A8', 'SIB553A5', 'SER303A3', 'SIB351A21', 'SIB553A16', 'SIB255A1', 'SIB608A1', 'SIB351A24', 'SIB501A2', 'SIB403A25', 'SIB501A3', 'SER303A7', 'SIB603A11', 'AND51A4', 'SIB553A25', 'SIB502A2', 'SIB501A4', 'SER303A8', 'SIB652A2', 'SIB257A24', 'AND51A1', 'BRA1907A6', 'AND51A5', 'SIB501A1', 'SIB601A8', 'SIB257A22', 'SIB653A1', 'SER307A2', 'SER303A6', 'SIB351A20', 'SER307A3', 'SIB553A6', 'ADM1852A4', 'SIB601A6', 'SIB404A21', 'SER303A4', 'SER303A5', 'SER303A2', 'SIB601A10', 'SIB553A26', 'SER307A5', 'SIB553A1', 'SIB253A1', 'SIB351A23', 'SIB253A2', 'SIB404A22', 'SIB601A3', 'SIB553A4', 'SIB702A1', 'ADM1851A3', 'SIB552A14', 'AND51A6', 'SIB609A1', 'SER307A6', 'SIB606A1', 'SIB611A2', 'SIB553A22', 'SIB255A3', 'SIB603A17', 'SIB253A3', 'ADM1851A2', 'SIB601A13', 'SIB553A18', 'AND51A2', 'SIB403A26', 'SIB552A9', 'SIB553A2', 'SIB553A20', 'SER307A1', 'SIB553A21', 'SIB404A20', 'SIB663A3', 'SIB404A24', 'ADM990A1', 'SIB603A7', 'SIB404A23', 'SIB553A23', 'SIB552A7', 'SIB502A1', 'SIB351A19', 'SIB552A1', 'SIB601A9', 'ADM1851A1', 'SIB553A11', 'SIB255A2']

YEARS = [str(y) for y in range(2017, THIS_YEAR + 1)]

LANE_UDFS = ['% Aligned R1', '% Aligned R2', '% Bases >=Q30 R1', '% Bases >=Q30 R2', '% Error Rate R1', '% Error Rate R2', '% Phasing R1', '% Prephasing R1', '% Prephasing R2', '%PF R1', '%PF R2', 'Cluster Density (K/mm^2) R1', 'Cluster Density (K/mm^2) R2', 'Intensity Cycle 1 R1', 'Intensity Cycle 1 R2', 'Reads PF (M) R1', 'Reads PF (M) R2', 'Yield PF (Gb) R1', 'Yield PF (Gb) R2', '% Phasing R2']

RUN_TYPES = ['AUTOMATED - NovaSeq Run',  'CG002 - Illumina Sequencing (Illumina SBS)', 'CG002 - Illumina Sequencing (HiSeq X)']

PICARD_INSERT_SIZE = [ 'MEDIAN_INSERT_SIZE', 'MODE_INSERT_SIZE', 'MEDIAN_ABSOLUTE_DEVIATION', 'MIN_INSERT_SIZE', 'MAX_INSERT_SIZE', 'MEAN_INSERT_SIZE', 'STANDARD_DEVIATION', 'READ_PAIRS', 'PAIR_ORIENTATION', 'WIDTH_OF_10_PERCENT', 'WIDTH_OF_20_PERCENT', 'WIDTH_OF_30_PERCENT', 'WIDTH_OF_40_PERCENT', 'WIDTH_OF_70_PERCENT', 'WIDTH_OF_80_PERCENT', 'WIDTH_OF_90_PERCENT', 'WIDTH_OF_50_PERCENT', 'WIDTH_OF_60_PERCENT', 'WIDTH_OF_95_PERCENT', 'WIDTH_OF_99_PERCENT']
PICARD_HS_METRIC = ['PCT_EXC_DUPE', 'PCT_EXC_MAPQ', 'PCT_EXC_BASEQ', 'PCT_EXC_OVERLAP', 'PCT_EXC_OFF_TARGET', 'FOLD_80_BASE_PENALTY', 'PCT_TARGET_BASES_1X', 'PCT_TARGET_BASES_2X', 'PCT_TARGET_BASES_10X', 'PCT_TARGET_BASES_20X', 'PCT_TARGET_BASES_30X', 'PCT_TARGET_BASES_40X', 'PCT_TARGET_BASES_50X', 'PCT_TARGET_BASES_100X', 'HS_LIBRARY_SIZE', 'HS_PENALTY_10X', 'HS_PENALTY_20X', 'HS_PENALTY_30X', 'HS_PENALTY_40X', 'HS_PENALTY_50X', 'HS_PENALTY_100X', 'AT_DROPOUT', 'GC_DROPOUT', 'HET_SNP_SENSITIVITY', 'HET_SNP_Q', 'SAMPLE', 'LIBRARY', 'READ_GROUP', 'BAIT_SET', 'TARGET_TERRITORY', 'BAIT_DESIGN_EFFICIENCY', 'TOTAL_READS', 'PF_READS', 'PF_UNIQUE_READS', 'PCT_PF_READS', 'PCT_PF_UQ_READS', 'PF_UQ_READS_ALIGNED', 'PCT_PF_UQ_READS_ALIGNED', 'PF_BASES_ALIGNED', 'PF_UQ_BASES_ALIGNED', 'ON_BAIT_BASES', 'NEAR_BAIT_BASES', 'OFF_BAIT_BASES', 'ON_TARGET_BASES', 'PCT_SELECTED_BASES', 'PCT_OFF_BAIT', 'ON_BAIT_VS_SELECTED', 'MEAN_BAIT_COVERAGE', 'MEAN_TARGET_COVERAGE', 'MEDIAN_TARGET_COVERAGE', 'MAX_TARGET_COVERAGE', 'PCT_USABLE_BASES_ON_BAIT', 'PCT_USABLE_BASES_ON_TARGET', 'FOLD_ENRICHMENT', 'ZERO_CVG_TARGETS_PCT', 'GENOME_SIZE', 'BAIT_TERRITORY']

INSTRUMENTS ={'D00410':'Sigourney', 
                'D00415':'Merida',
                'D00450': 'Arnold',
                'ST-E00198':'Dorothy',
                'ST-E00201':'Irene',
                'ST-E00214':'Marie',
                'ST-E00266':'Rita',
                'ST-E00269':'Rosalyn',
                'A00187':'Ingrid',
                'A00689':'Barbara',
                'A00621':'Greta',
                'FS10000534':'Katherine'}


MICROSALT = {
        'picard_markduplicate': 
                {'insert_size': 'Median distance between read 1 and read 2 of paired reads. Trimmed deduplicated reads mapped via bwa, reported in Picard. Result is extrapolated from curve fitting the data.', 
                'duplication_rate':'Percentage of reads that were exact duplicates (thus giving no new information). Trimmed reads mapped via bwa, reported in picard'}, 
        'microsalt_samtools_stats':
                {'average_coverage':'Summed coverage of each position, divided by reference genome length. Trimmed deduplicated reads mapped via bwa, reported in  Samtools', 
                'coverage_10x':'Number of positions above 10x coverage, divided by genome length	Trimmed deduplicated reads mapped via bwa, reported in  Samtools', 
                'coverage_30x':'Number of positions above 30x coverage, divided by genome length	Trimmed deduplicated reads mapped via bwa, reported in  Samtools', 
                'coverage_50x':'Number of positions above 50x coverage, divided by genome length	Trimmed deduplicated reads mapped via bwa, reported in  Samtools', 
                'coverage_100x':'Number of positions above 100x coverage, divided by genome length	Trimmed deduplicated reads mapped via bwa, reported in  Samtools', 
                'total_reads':'Number of reads	Trimmed reads mapped via bwa, reported in samtools.',
                'mapped_rate': 'Percentage of reads that mapped to the reference. Trimmed reads mapped via bwa, reported in samtools.'}, 
        'quast_assembly':
                {'necessary_contigs', 
                'gc_percentage', 
                'estimated_genome_length', 
                'n50'}
        }
