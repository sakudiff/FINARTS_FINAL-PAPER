library(tidyverse, warn.conflicts = FALSE)
Sys.setlocale("LC_TIME", "C")

df <- read_csv("data/processed/final_dataset.csv", show_col_types = FALSE)

# Extract risk_off=1 dates, group consecutive runs, merge episodes within 10 days
risk_dates <- df |>
  filter(risk_off == 1) |>
  select(date) |>
  mutate(
    gap = date - lag(date, default = first(date) - 1),
    episode = cumsum(gap > 1)
  ) |>
  group_by(episode) |>
  summarise(start = min(date), end = max(date), days = n(), .groups = "drop") |>
  # Merge episodes within 10-day gap
  arrange(start) |>
  mutate(
    merge_gap = start - lag(end, default = first(start) - 11),
    merge_group = cumsum(merge_gap > 10)
  ) |>
  group_by(merge_group) |>
  summarise(
    start = min(start),
    end   = max(end),
    days  = sum(days),
    .groups = "drop"
  ) |>
  mutate(
    event = case_when(
      start <= as.Date("2000-10-31") & end <= as.Date("2000-12-31") ~ "Dot-com crash / Tech sell-off",
      start <= as.Date("2001-12-31") & end <= as.Date("2001-12-31") ~ "9/11 attacks & aftermath",
      start <= as.Date("2002-12-31") & end <= as.Date("2002-12-31") ~ "Corporate scandals (WorldCom, Enron)",
      start <= as.Date("2006-07-31") & end <= as.Date("2006-07-31") ~ "Geopolitical tensions (Iran / NK)",
      start <= as.Date("2007-12-31") & end <= as.Date("2007-12-31") ~ "BNP Paribas freezes funds / GFC onset",
      start <= as.Date("2008-12-31") & end <= as.Date("2008-12-31") & days > 10 ~ "Global Financial Crisis (Lehman collapse)",
      start <= as.Date("2008-12-31") ~ "Global Financial Crisis",
      start <= as.Date("2010-06-30") ~ "Flash Crash / Eurozone debt crisis",
      start <= as.Date("2011-04-30") ~ "Tohoku earthquake & tsunami",
      start <= as.Date("2011-12-31") ~ "US debt ceiling / Eurozone sovereign crisis",
      start <= as.Date("2014-12-31") ~ "Ebola / Oil price collapse",
      start <= as.Date("2016-12-31") & end <= as.Date("2016-12-31") ~ "China crash (Black Monday) / Brexit",
      start <= as.Date("2018-02-28") ~ "Volmageddon (Volatility spike)",
      start <= as.Date("2018-12-31") & end <= as.Date("2018-12-31") ~ "Trade war / Tech sell-off",
      start <= as.Date("2020-12-31") & days > 20 ~ "COVID-19 global pandemic",
      start <= as.Date("2020-12-31") ~ "COVID-19 pandemic",
      start <= as.Date("2021-06-30") ~ "GameStop short squeeze / Retail mania",
      start <= as.Date("2022-02-28") ~ "Omicron variant / Fed hawkish pivot",
      start <= as.Date("2022-12-31") ~ "Russia-Ukraine war / Commodity crisis",
      start <= as.Date("2024-09-30") ~ "Yen carry trade unwind / Global sell-off",
      start <= as.Date("2025-02-28") ~ "Fed hawkish pause / BOJ policy divergence",
      start <= as.Date("2025-06-30") ~ '"America First" trade policy / Tariff war',
      start >= as.Date("2026-03-01") ~ "Iran conflict / Middle East escalation",
      TRUE ~ "Other"
    )
  )

rows <- risk_dates |>
  mutate(
    date_range = ifelse(
      start == end,
      format(start, "%b %d, %Y"),
      paste0(format(start, "%b %d, %Y"), " -- ", format(end, "%b %d, %Y"))
    ),
    line = paste0("  ", date_range, " & ", days, " & ", str_replace_all(event, "&", "\\\\&"), " \\\\")
  )

bs <- "\\"

preamble <- c(
  paste0(bs, "documentclass[10pt]{article}"),
  paste0(bs, "usepackage[utf8]{inputenc}"),
  paste0(bs, "usepackage[margin=0.3in,landscape]{geometry}"),
  paste0(bs, "usepackage{booktabs}"),
  paste0(bs, "usepackage{longtable}"),
  "",
  paste0(bs, "begin{document}"),
  paste0(bs, "pagestyle{empty}"),
  paste0(bs, "small"),
  paste0(bs, "setlength{", bs, "tabcolsep}{4pt}"),
  paste0(bs, "renewcommand{", bs, "arraystretch}{0.85}"),
  "",
  paste0(bs, "begin{longtable}{l r p{8cm}}"),
  paste0("  ", bs, "caption*{Risk-off Episodes (VIX ", bs, "ge MA60 + 10)} \\\\"),
  paste0("  ", bs, "toprule"),
  "  \\textbf{Dates} & \\textbf{Days} & \\textbf{Event / Interpretation} \\\\",
  paste0("  ", bs, "midrule"),
  paste0("  ", bs, "endfirsthead"),
  paste0("  ", bs, "toprule"),
  "  \\textbf{Dates} & \\textbf{Days} & \\textbf{Event / Interpretation} \\\\",
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
writeLines(c(preamble, rows$line, closing), "drafts/risk_off_episodes.tex")
cat("Written:", nrow(rows), "episodes to drafts/risk_off_episodes.tex\n")
cat(rows$event |> table() |> paste(collapse = "\n"), "\n")
