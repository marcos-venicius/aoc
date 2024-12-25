defmodule Aoc do
  @input_file "input.txt"

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
  end

  defp handle_result({:error, _} = error), do: error

  defp handle_result({left_digits, right_digits}) do
    {Enum.sort(left_digits), Enum.sort(right_digits)}
  end

  defp diff({:error, _} = error), do: error

  defp diff({left_digits, right_digits}) do
    Enum.zip(left_digits, right_digits)
    |> Enum.map(fn {left, right} -> abs(right - left) end)
  end

  defp sum({:error, _} = error), do: error
  defp sum([]), do: 0
  defp sum([head | tail]), do: head + sum(tail)

  defp calc_score({:error, _} = error), do: error

  defp calc_score({[], _}), do: 0

  defp calc_score({[head | left_digits], right_digits}) do
    head * Enum.count(right_digits, fn x -> x == head end) +
      calc_score({left_digits, right_digits})
  end

  def part_one() do
    case File.read(@input_file) do
      {:ok, content} ->
        content
        |> extract_digits()
        |> diff()
        |> sum()
        |> case do
          {:error, message} -> IO.puts("Could not run part one due to: #{message}")
          ans -> IO.puts("Part 01: #{ans}")
        end

      {:error, reason} ->
        IO.puts("Failed to read input due to: #{reason}")
    end
  end

  def part_two() do
    case File.read(@input_file) do
      {:ok, content} ->
        content
        |> extract_digits()
        |> calc_score()
        |> case do
          {:error, message} -> IO.puts("Could not run part two due to: #{message}")
          ans -> IO.puts("Part 02: #{ans}")
        end

      {:error, reason} ->
        IO.puts("Failed to read input due to: #{reason}")
    end
  end
end

Aoc.part_one()
Aoc.part_two()
