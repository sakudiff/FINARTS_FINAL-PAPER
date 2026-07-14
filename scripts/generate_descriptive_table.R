library(tidyverse, warn.conflicts = FALSE)

# Read descriptive statistics from pipeline output
desc <- read_csv("data/processed/descriptive_stats.csv", show_col_types = FALSE)

colnames(desc) <- c("Variable", "Stat", "Paper", "Extended", "Full")

# Generate LaTeX rows
rows <- desc |>
  mutate(Variable = str_replace_all(Variable, "_", "\\\\_")) |>
  group_by(Variable) |>
  mutate(row_number = row_number()) |>
  ungroup() |>
  mutate(
    display_var = ifelse(row_number == 1, Variable, ""),
    paper  = ifelse(Stat == "N", sprintf("%s", Paper), sprintf("%8.4f", Paper)),
    ext    = ifelse(Stat == "N", sprintf("%s", Extended), sprintf("%8.4f", Extended)),
    full   = ifelse(Stat == "N", sprintf("%s", Full), sprintf("%8.4f", Full))
  )

# Write LaTeX file
cat("\\documentclass[10pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[margin=0.3in]{geometry}
\\usepackage{booktabs}
\\usepackage{longtable}

\\begin{document}
\\pagestyle{empty}
\\setlength{\\tabcolsep}{4pt}
\\renewcommand{\\arraystretch}{0.85}

\\begin{longtable}{l l r r r}
\\caption*{Descriptive Statistics by Period} \\\\
\\toprule
\\textbf{Variable} & \\textbf{Stat} & \\textbf{1999--2021 (Paper)} & \\textbf{2021--2026 (Extended)} & \\textbf{Full Sample} \\\\
\\midrule
\\endfirsthead
\\toprule
\\textbf{Variable} & \\textbf{Stat} & \\textbf{1999--2021 (Paper)} & \\textbf{2021--2026 (Extended)} & \\textbf{Full Sample} \\\\
\\midrule
\\endhead
\\bottomrule
\\endfoot
\\bottomrule
\\endlastfoot
", file = "drafts/descriptive_stats_table.tex")

# Write each row group
current_var <- ""
for (i in seq_len(nrow(rows))) {
  r <- rows[i, ]
  sep <- ifelse(r$row_number == 1 && i > 1, "\\addlinespace\n", "")
  line <- sprintf("%s%-15s & %-5s & %10s & %10s & %10s \\\\\n",
    sep, r$display_var, r$Stat, r$paper, r$ext, r$full)
  cat(line, file = "drafts/descriptive_stats_table.tex", append = TRUE)
}

cat("\\end{longtable}

\\end{document}
", file = "drafts/descriptive_stats_table.tex", append = TRUE)

cat("LaTeX table written to drafts/descriptive_stats_table.tex\n")
