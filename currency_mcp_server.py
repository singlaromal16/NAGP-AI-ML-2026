import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Currency Server",
    instructions=(
        "This MCP server provides currency conversion tools. "
        "Use convert_currency to convert amounts between different currencies."
    ),
)

@mcp.tool(
    description=(
        "Convert an amount from one currency to another "
        "using current exchange-rate information."
    )
)
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> dict:
    """Convert currency using an external exchange-rate service."""

    if amount < 0:
        return {
            "success": False,
            "error": "Amount cannot be negative."
        }

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    try:
        response = httpx.get(
            "https://api.frankfurter.app/latest",
            params={
                "amount": amount,
                "from": from_currency,
                "to": to_currency,
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if to_currency not in data.get("rates", {}):
            return {
                "success": False,
                "error": (
                    f"Unable to convert "
                    f"{from_currency} to {to_currency}."
                )
            }

        converted_amount = data["rates"][to_currency]

        return {
            "success": True,
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": converted_amount,
            "rate_date": data.get("date"),
            "source": "Frankfurter via Currency MCP",
        }

    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"Currency service failed: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run()