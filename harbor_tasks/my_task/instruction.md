# Service Window Merge

Read `/app/input.txt`, consolidate approved maintenance windows, and write the result to `/app/output.json`.

## Input schema

The input is a JSON array. Each element contains:

- `service` (string): service name
- `start_minute` (integer): inclusive start
- `end_minute` (integer): exclusive end
- `status` (string): approval state

## Transformation rules

1. Keep only entries whose `status` is exactly `"approved"`.
2. Group the remaining windows by `service`.
3. Merge windows that overlap or touch. For example, `[10, 20]` and `[20, 35]` become `[10, 35]`.
4. For each service, produce:
   - `service`: the service name
   - `windows`: merged intervals as arrays of `[start_minute, end_minute]`
   - `total_minutes`: sum of the merged interval lengths
   - `longest_minutes`: length of the longest merged interval
5. Sort services lexicographically by `service`.
6. Sort each service's merged windows by start minute.
7. Do not include services with no approved windows.

Write the result as a JSON array to `/app/output.json`. Use two-space indentation and include a trailing newline. Do not include extra fields.
