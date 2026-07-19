# Risk-off Reference Charts and Appendix Figures
# Beirne & Sugandi (2023) Replication
#
# Generates:
# - Figure 1: VIX, 60-day MA, and risk-off episodes (compare paper Figure 1)
# - Figure 2: USD/JPY and risk-off episodes (compare paper Figure 2)
# - Figure 3: Japan REER and risk-off episodes (compare paper Figure 3)
# - Figure A1.1: JGB 10Y and risk-off episodes
# - Figure A1.2: Nikkei 225 and risk-off episodes
# - Figure A1.3-A1.6: Capital flows and risk-off episodes
# - Figure A1.7: Yield spread and risk-off episodes

library(tidyverse)
library(readxl)
library(zoo)
library(lubridate)

DATA_RAW <- file.path("data", "raw")
FIG_DIR  <- file.path("data", "processed", "var_results", "figures")
dir.create(FIG_DIR, showWarnings = FALSE, recursive = TRUE)

START_DATE <- as.Date("1999-01-01")
END_DATE   <- as.Date("2026-06-30")
PAPER_END  <- as.Date("2021-03-31")

chicago_45   <- "#2E45B8"
singapore_55 <- "#F97A1F"
tokyo_45     <- "#C91D42"
london_5     <- "#0D0D0D"
london_35    <- "#595959"
london_85    <- "#D9D9D9"
london_95    <- "#F2F2F2"
bg_color     <- "#F5F4EF"

theme_risk <- function() {
  theme_minimal() +
    theme(
      text = element_text(color = london_5),
      plot.title = element_text(face = "bold", size = 11, margin = margin(b = 4)),
      plot.subtitle = element_text(size = 9, color = london_35, margin = margin(b = 6)),
      plot.caption = element_text(size = 7, color = london_35, hjust = 0, margin = margin(t = 4)),
      axis.title = element_text(size = 8, color = london_35),
      axis.text = element_text(size = 7, color = london_35),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(color = london_95, linewidth = 0.3),
      plot.background = element_rect(fill = bg_color, color = NA),
      panel.background = element_rect(fill = bg_color, color = NA),
      legend.position = "bottom",
      legend.text = element_text(size = 7),
      legend.title = element_blank(),
      axis.ticks = element_blank(),
      plot.margin = margin(10, 10, 10, 10)
    )
}

# Load data
vix <- read_csv(file.path(DATA_RAW, "VIX.csv"),
                col_types = cols(Date = col_date(), Close = col_double()),
                show_col_types = FALSE) |>
  rename(date = Date, vix = Close)

# USD/JPY
usdjpy <- read_csv(file.path(DATA_RAW, "USDJPY.csv"),
                   col_types = cols(Date = col_date(), Close = col_double()),
                   show_col_types = FALSE) |>
  rename(date = Date, usdjpy = Close)

# REER
reer_sheets <- excel_sheets(file.path(DATA_RAW, "REER.xlsx"))
reer_raw <- read_excel(file.path(DATA_RAW, "REER.xlsx"),
                      sheet = reer_sheets[1], col_types = "text")
reer <- reer_raw |>
  filter(!is.na(.data[[names(reer_raw)[1]]])) |>
  rename(date_raw = 1, reer = 2) |>
  mutate(date = as_date(ymd_hms(date_raw)), reer = as.numeric(reer)) |>
  select(date, reer) |>
  arrange(date)

# JGB 10Y from daily curve data
jgb_raw <- read_csv(file.path(DATA_RAW, "jgbcme_all.csv"),
                    skip = 1, show_col_types = FALSE) |>
  rename(date = Date) |>
  mutate(date = ymd(date))
jgb10y <- jgb_raw |>
  select(date, jgb10y = all_of(names(jgb_raw)[11])) |>
  mutate(jgb10y = as.numeric(na_if(jgb10y, "-")))

# Nikkei 225
nikkei <- read_csv(file.path(DATA_RAW, "NIKKEI225.csv"),
                   col_types = cols(Date = col_date(), Close = col_double()),
                   show_col_types = FALSE) |>
  rename(date = Date, nikkei = Close)

# US 10Y for spread
us10y <- read_csv(file.path(DATA_RAW, "US10Y.csv"),
                  col_types = cols(Date = col_date(), Close = col_double()),
                  show_col_types = FALSE) |>
  rename(date = Date, us10y = Close)

# Load final dataset for capital flow %GDP
final <- read_csv(file.path("data", "processed", "final_dataset.csv"),
                  show_col_types = FALSE) |>
  mutate(date = as_date(date))

# Calculate risk-off binary and VIX MA
vix <- vix |>
  arrange(date) |>
  mutate(
    vix_ma60 = rollmean(vix, k = 60, fill = NA, align = "right"),
    risk_off = if_else(vix >= vix_ma60 + 10, 1L, 0L)
  )

# Filter to plot range
plot_range <- function(df) df |> filter(date >= START_DATE, date <= END_DATE)

plot_risk_off_series <- function(data, y_col, y_label, title, caption) {
  ro_episodes <- data |>
    filter(risk_off == 1) |>
    mutate(episode_id = cumsum(c(1, diff(date) > 10))) |>
    group_by(episode_id) |>
    summarise(start = min(date), end = max(date), .groups = "drop")

  ggplot() +
    geom_rect(data = ro_episodes,
              aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf,
                  fill = "Risk-off episode"),
              alpha = 0.12, na.rm = TRUE) +
    geom_line(data = data, aes(x = date, y = .data[[y_col]]),
              color = chicago_45, linewidth = 0.5) +
    geom_hline(yintercept = 0, color = london_85, linewidth = 0.3) +
    scale_fill_manual(values = c("Risk-off episode" = tokyo_45)) +
    labs(title = title, x = NULL, y = y_label) +
    scale_x_date(limits = c(START_DATE, END_DATE),
                 breaks = seq(START_DATE, END_DATE, by = "5 years"),
                 date_labels = "%Y") +
    theme_risk()
}

# Figure 1: VIX, 60-day MA, Risk-off episodes
vix_plot <- vix |> filter(date >= START_DATE)
vix_ro <- vix_plot |>
  filter(risk_off == 1) |>
  mutate(ep = cumsum(c(1, diff(date) > 10))) |>
  group_by(ep) |>
  summarise(start = min(date), end = max(date), .groups = "drop")

p1 <- ggplot() +
  geom_rect(data = vix_ro,
            aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf, fill = "Risk-off episode"),
            alpha = 0.12) +
  geom_line(data = vix_plot, aes(x = date, y = vix, color = "VIX"),
            linewidth = 0.4) +
  geom_line(data = vix_plot, aes(x = date, y = vix_ma60, color = "60-day MA"),
            linewidth = 0.4, alpha = 0.8) +
  scale_color_manual(values = c("VIX" = chicago_45, "60-day MA" = singapore_55)) +
  scale_fill_manual(values = c("Risk-off episode" = tokyo_45)) +
  guides(color = guide_legend(order = 1), fill = guide_legend(order = 2)) +
  labs(
    title = "VIX, 60-day moving average, and risk-off episodes",
    subtitle = "Shaded regions denote risk-off episodes (VIX >= 60-day MA + 10pp).",
    x = NULL, y = "VIX index"
  ) +
  scale_x_date(limits = c(START_DATE, END_DATE),
               breaks = seq(START_DATE, END_DATE, by = "5 years"),
               date_labels = "%Y") +
  theme_risk()

ggsave(file.path(FIG_DIR, "fig1_vix_risk_off.png"), p1, width = 10, height = 4, dpi = 150)
cat("Saved: fig1_vix_risk_off.png\n")

# Figure 2: USD/JPY and risk-off episodes
# Merge USD/JPY with risk-off dates
usdjpy_plot <- usdjpy |>
  left_join(vix |> select(date, risk_off), by = "date") |>
  filter(date >= START_DATE)

p2 <- plot_risk_off_series(usdjpy_plot, "usdjpy", "JPY per USD",
  "Bilateral nominal USD/JPY exchange rate and risk-off episodes",
  "Source: Bloomberg. Authors' calculation.")
ggsave(file.path(FIG_DIR, "fig2_usdjpy_risk_off.png"), p2, width = 10, height = 4, dpi = 150)
cat("Saved: fig2_usdjpy_risk_off.png\n")

# Figure 3: REER and risk-off episodes
reer_plot <- reer |>
  left_join(vix |> select(date, risk_off), by = "date") |>
  filter(date >= START_DATE)

p3 <- plot_risk_off_series(reer_plot, "reer", "REER (2010 = 100)",
  "Japan's real effective exchange rate and risk-off episodes",
  "Source: BIS. Authors' calculation.")
ggsave(file.path(FIG_DIR, "fig3_reer_risk_off.png"), p3, width = 10, height = 4, dpi = 150)
cat("Saved: fig3_reer_risk_off.png\n")

# Figure A1.1: JGB 10Y and risk-off episodes
jgb_plot <- jgb10y |>
  left_join(vix |> select(date, risk_off), by = "date") |>
  filter(date >= START_DATE)

p_a1 <- plot_risk_off_series(jgb_plot, "jgb10y", "Percent",
  "10-year JGB yields and risk-off episodes",
  "Source: Bloomberg. Authors' calculation.")
ggsave(file.path(FIG_DIR, "figA1_1_jgb_risk_off.png"), p_a1, width = 10, height = 4, dpi = 150)
cat("Saved: figA1_1_jgb_risk_off.png\n")

# Figure A1.2: Nikkei 225 and risk-off episodes
nikkei_plot <- nikkei |>
  left_join(vix |> select(date, risk_off), by = "date") |>
  filter(date >= START_DATE)

p_a2 <- plot_risk_off_series(nikkei_plot, "nikkei", "Index value",
  "Nikkei-225 index and risk-off episodes",
  "Source: Bloomberg. Authors' calculation.")
ggsave(file.path(FIG_DIR, "figA1_2_nikkei_risk_off.png"), p_a2, width = 10, height = 4, dpi = 150)
cat("Saved: figA1_2_nikkei_risk_off.png\n")

# Figures A1.3-A1.6: Capital flows and risk-off episodes
flow_vars <- c("debtsec_pct", "equity_pct", "other_pct", "direct_pct")
flow_labels <- c("Net debt securities investment to Japan (% of GDP)",
                 "Net equity investment to Japan (% of GDP)",
                 "Net other investment to Japan (% of GDP)",
                 "Net direct investment to Japan (% of GDP)")
flow_files <- c("figA1_3_debtsec_risk_off.png", "figA1_4_equity_risk_off.png",
                "figA1_5_other_risk_off.png", "figA1_6_direct_risk_off.png")
flow_captions <- c("Source: Bloomberg. Authors' calculation.",
                   "Source: Bloomberg. Authors' calculation.",
                   "Source: Bloomberg. Authors' calculation.",
                   "Source: Bloomberg. Authors' calculation.")

for (i in seq_along(flow_vars)) {
  plot_data <- final |>
    select(date, value = all_of(flow_vars[i]), risk_off) |>
    filter(!is.na(value))

  ro_bands <- plot_data |>
    filter(risk_off == 1) |>
    mutate(ep = cumsum(c(1, diff(date) > 10))) |>
    group_by(ep) |> summarise(start = min(date), end = max(date), .groups = "drop")

  p <- ggplot() +
    geom_rect(data = ro_bands,
              aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf,
                  fill = "Risk-off episode"),
              alpha = 0.12) +
    geom_line(data = plot_data, aes(x = date, y = value),
              color = chicago_45, linewidth = 0.4) +
    geom_hline(yintercept = 0, color = london_85, linewidth = 0.3) +
    scale_fill_manual(values = c("Risk-off episode" = tokyo_45)) +
    labs(title = flow_labels[i], x = NULL, y = "Percent of GDP") +
    scale_x_date(limits = c(START_DATE, END_DATE),
                 breaks = seq(START_DATE, END_DATE, by = "5 years"),
                 date_labels = "%Y") +
    theme_risk()

  ggsave(file.path(FIG_DIR, flow_files[i]), p, width = 10, height = 4, dpi = 150)
  cat("Saved:", flow_files[i], "\n")
}

# Figure A1.7: Yield spread (JGB 10Y - US 10Y) and risk-off episodes
spread_plot <- final |>
  select(date, spread, risk_off) |>
  filter(!is.na(spread))

ro_spread <- spread_plot |>
  filter(risk_off == 1) |>
  mutate(ep = cumsum(c(1, diff(date) > 10))) |>
  group_by(ep) |> summarise(start = min(date), end = max(date), .groups = "drop")

p_a7 <- ggplot() +
  geom_rect(data = ro_spread,
            aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf,
                fill = "Risk-off episode"),
            alpha = 0.12) +
  geom_line(data = spread_plot, aes(x = date, y = spread),
            color = chicago_45, linewidth = 0.4) +
  geom_hline(yintercept = 0, color = london_85, linewidth = 0.3) +
  scale_fill_manual(values = c("Risk-off episode" = tokyo_45)) +
  labs(title = "Yield spread between 10-year US and Japan government bonds",
       x = NULL, y = "Percentage points") +
  scale_x_date(limits = c(START_DATE, END_DATE),
               breaks = seq(START_DATE, END_DATE, by = "5 years"),
               date_labels = "%Y") +
  theme_risk()

ggsave(file.path(FIG_DIR, "figA1_7_spread_risk_off.png"), p_a7, width = 10, height = 4, dpi = 150)
cat("Saved: figA1_7_spread_risk_off.png\n")

cat("\nAll risk-off reference charts generated.\n")
