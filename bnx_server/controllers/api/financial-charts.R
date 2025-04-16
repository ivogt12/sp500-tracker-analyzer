# Suppress package loading messages
suppressMessages(library(jsonlite))
suppressMessages(library(ggplot2))
suppressMessages(library(dplyr))
suppressMessages(library(tidyr))
suppressMessages(library(Cairo))  # For better plot rendering

# Ignore all errors and exit with status 0
try({

  # -------------------------
  # 1. Read JSON Data
  # -------------------------
  args <- commandArgs(trailingOnly = TRUE)
  json_path <- args[1]
  plot_dir <- args[2]

  # Create plot directory if it doesn't exist
  if (!dir.exists(plot_dir)) {
    dir.create(plot_dir, recursive = TRUE)
  }

  # Read and parse JSON data
  data <- fromJSON(json_path)

  # -------------------------
  # 2. Clean Numeric Values Utility
  # -------------------------
  clean_numeric <- function(x) {
    sapply(x, function(value) {
      if (is.null(value) || is.na(value)) {
        return(NA_real_)
      } else {
        value <- gsub("\\s+", "", value)
        if (grepl("M", value, ignore.case = TRUE)) {
          return(as.numeric(gsub("[^0-9.]", "", value)) * 1e6)
        } else if (grepl("B", value, ignore.case = TRUE)) {
          return(as.numeric(gsub("[^0-9.]", "", value)) * 1e9)
        } else {
          return(as.numeric(gsub("[^0-9.]", "", value)))
        }
      }
    })
  }

  # -------------------------
  # 3. Financial Ratios Plot
  # -------------------------
  financial_ratios <- data %>%
    select(trailingPeRatio, forwardPeRatio, pbRatio, roe, roa, debtToEquity) %>%
    mutate(across(everything(), clean_numeric))

  ratios_df <- financial_ratios %>%
    pivot_longer(everything(), names_to = "Metric", values_to = "Value") %>%
    filter(!is.na(Value))

  plot1 <- ggplot(ratios_df, aes(x = Metric, y = Value, fill = Metric)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    theme(legend.position = "none") +
    labs(title = "Financial Ratios Comparison", x = "Metric", y = "Value")

  CairoPNG(filename = file.path(plot_dir, "financial_ratios_plot.png"), width = 800, height = 600)
  print(plot1)
  dev.off()

  # -------------------------
  # 4. Revenue vs Net Income Plot
  # -------------------------
  dates <- unlist(data$date)
  total_revenue <- clean_numeric(unlist(data$totalRevenue))
  net_income <- clean_numeric(unlist(data$netIncomeCommStockHolders))

  rev_df <- data.frame(
    Date = factor(dates, levels = dates),
    TotalRevenue = total_revenue,
    NetIncome = net_income
  )

  scaleFactor <- max(rev_df$TotalRevenue, na.rm = TRUE) / max(rev_df$NetIncome, na.rm = TRUE)
  plot2 <- ggplot(rev_df, aes(x = Date)) +
    geom_line(aes(y = TotalRevenue, color = "Total Revenue")) +
    geom_line(aes(y = NetIncome * scaleFactor, color = "Net Income")) +
    scale_y_continuous(
      name = "Total Revenue",
      sec.axis = sec_axis(~ ./scaleFactor, name = "Net Income")
    ) +
    theme_minimal() +
    labs(title = "Revenue vs Net Income Growth", x = "Date")

  CairoPNG(filename = file.path(plot_dir, "revenue_net_income_dual_axis.png"), width = 800, height = 600)
  print(plot2)
  dev.off()

  # -------------------------
  # 5. Cash Flow & Balance Sheet Plot
  # -------------------------
  cash_flow <- data %>%
    select(operatingCashFlow, investingCashFlow, financingCashFlow, freeCashFlow) %>%
    mutate(across(everything(), clean_numeric))

  balance_sheet <- data %>%
    select(totalAssets, totalLiabilities, shareholderEquity) %>%
    mutate(across(everything(), clean_numeric))

  cash_flow_df <- cash_flow %>%
    pivot_longer(everything(), names_to = "Metric", values_to = "Value") %>%
    mutate(Category = "Cash Flow")

  balance_sheet_df <- balance_sheet %>%
    pivot_longer(everything(), names_to = "Metric", values_to = "Value") %>%
    mutate(Category = "Balance Sheet")

  combined_df <- bind_rows(cash_flow_df, balance_sheet_df) %>% na.omit()

  plot3 <- ggplot(combined_df, aes(x = Category, y = Value, fill = Metric)) +
    geom_bar(stat = "identity", position = "dodge") +
    theme_minimal() +
    labs(title = "Cash Flow & Balance Sheet Analysis", x = "Category", y = "Value")

  CairoPNG(filename = file.path(plot_dir, "cash_flow_balance_sheet.png"), width = 800, height = 600)
  print(plot3)
  dev.off()

}, silent = TRUE)  # Ignore all errors

# Always exit with code 0
quit(status = 0)
