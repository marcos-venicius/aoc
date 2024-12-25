defmodule Aoc do
  def extract_digits(string) do
    string
    |> String.split("\n", trim: true)
    |> Enum.reduce({[], []}, fn line, {left_digits, right_digits} ->
      case Regex.run(~r/(\d+)\s+(\d+)/, line) do
        [_, left_digit, right_digit] ->
          {
            left_digits ++ [String.to_integer(left_digit)],
            right_digits ++ [String.to_integer(right_digit)]
          }

        _ ->
          {:error, "Invalid format in line #{line}"}
      end
    end)
    |> handle_result()
    |> diff()
    |> sum()
  end

  defp handle_result({:error, _} = error), do: error

  defp handle_result({left_digits, right_digits}) do
    {:ok, Enum.sort(left_digits), Enum.sort(right_digits)}
  end

  defp diff({:error, _} = error), do: error

  defp diff({:ok, left_digits, right_digits}) do
    {:ok,
     Enum.zip(left_digits, right_digits)
     |> Enum.map(fn {left, right} -> abs(right - left) end)}
  end

  defp sum({:error, _} = error), do: error
  defp sum({:ok, []}), do: 0
  defp sum({:ok, [head | tail]}), do: head + sum({:ok, tail})

  def part_one() do
    case File.read("input.txt") do
      {:ok, content} ->
        content
        |> extract_digits
        |> case do
          {:error, message} -> IO.puts("Could not run part one due to: #{message}")
          ans -> IO.puts("Part 01: #{ans}")
        end

      {:error, reason} ->
        IO.puts("Failed to read input due to: #{reason}")
    end
  end
end

Aoc.part_one()
