library(tidyverse, warn.conflicts = FALSE)

desc <- read_csv("data/processed/descriptive_stats.csv", show_col_types = FALSE)

desc_wide <- desc |>
  pivot_longer(c(N, Mean, SD, Min, Max), names_to = "stat", values_to = "value") |>
  pivot_wider(names_from = period, values_from = value)

pn <- setdiff(names(desc_wide), c("variable", "stat"))

full_sample <- desc |>
  pivot_longer(c(N, Mean, SD, Min, Max), names_to = "stat", values_to = "value") |>
  group_by(variable, stat) |>
  summarise(full = mean(value, na.rm = TRUE), .groups = "drop")

rows <- desc_wide |>
  left_join(full_sample, by = c("variable", "stat")) |>
  mutate(variable = str_replace_all(variable, "_", "\\\\_")) |>
  group_by(variable) |>
  mutate(first = row_number() == 1) |>
  ungroup() |>
  rowwise() |>
  mutate(
    c1 = ifelse(stat == "N", as.character(round(.data[[pn[1]]], 0)), sprintf("%8.4f", .data[[pn[1]]])),
    c2 = ifelse(stat == "N", as.character(round(.data[[pn[2]]], 0)), sprintf("%8.4f", .data[[pn[2]]])),
    c3 = ifelse(stat == "N", as.character(round(full, 0)), sprintf("%8.4f", full))
  ) |>
  ungroup() |>
  mutate(line = paste0(
    ifelse(first & row_number() > 1, "\\addlinespace\n", ""),
    ifelse(first, sprintf("%-15s", variable), "               "),
    " & ", sprintf("%-5s", stat),
    " & ", sprintf("%10s", c1),
    " & ", sprintf("%10s", c2),
    " & ", sprintf("%10s", c3), "\\\\"
  ))

bs <- "\\"
nl <- paste0(bs, bs)

preamble <- c(
  paste0(bs, "documentclass[10pt]{article}"),
  paste0(bs, "usepackage[utf8]{inputenc}"),
  paste0(bs, "usepackage[margin=0.3in]{geometry}"),
  paste0(bs, "usepackage{booktabs}"),
  paste0(bs, "usepackage{longtable}"),
  "",
  paste0(bs, "begin{document}"),
  paste0(bs, "pagestyle{empty}"),
  paste0(bs, "setlength{", bs, "tabcolsep}{4pt}"),
  paste0(bs, "renewcommand{", bs, "arraystretch}{0.85}"),
  "",
  paste0(bs, "begin{longtable}{l l r r r}"),
  paste0("  ", bs, "caption*{Descriptive Statistics by Period} ", nl),
  paste0("  ", bs, "toprule"),
  paste0("  ", bs, "textbf{Variable} & ", bs, "textbf{Stat} & ",
    bs, "textbf{", pn[1], "} & ", bs, "textbf{", pn[2], "} & ",
    bs, "textbf{Full Sample} ", nl),
  paste0("  ", bs, "midrule"),
  paste0("  ", bs, "endfirsthead"),
  paste0("  ", bs, "toprule"),
  paste0("  ", bs, "textbf{Variable} & ", bs, "textbf{Stat} & ",
    bs, "textbf{", pn[1], "} & ", bs, "textbf{", pn[2], "} & ",
    bs, "textbf{Full Sample} ", nl),
  paste0("  ", bs, "midrule"),
  paste0("  ", bs, "endhead"),
  paste0("  ", bs, "bottomrule"),
  paste0("  ", bs, "endfoot"),
  paste0("  ", bs, "bottomrule"),
  paste0("  ", bs, "endlastfoot")
)

closing <- c(
  paste0(bs, "end{longtable}"),
  "",
  paste0(bs, "end{document}")
)

dir.create("drafts", showWarnings = FALSE)
tex_path <- file.path("drafts", "descriptive_stats_table.tex")
writeLines(c(preamble, rows$line, closing), tex_path)
cat("LaTeX table written to", tex_path, "\n")
