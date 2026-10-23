I’d use a REST API with an immutable stock ledger, current balances, and explicit reservations.

Assumptions: the service tracks discrete units by SKU and warehouse, supports checkout reservations, and prevents overselling. Purchasing, pricing, and warehouse picking are outside the initial scope.

### Core resources

| Resource | Purpose |
|---|---|
| **Item** | A stock-tracked SKU with an immutable ID and unique SKU code. |
| **Location** | A warehouse or other inventory holding location. |
| **Balance** | Current quantities for one item at one location. |
| **Reservation** | Stock held temporarily for an order or workflow. |
| **Movement** | An immutable record of stock received, shipped, adjusted, or transferred. |

Each balance contains:

```json
{
  "item_id": "itm_123",
  "location_id": "loc_456",
  "on_hand": 100,
  "reserved": 12,
  "available": 88,
  "updated_at": "2026-10-23T10:30:00Z"
}
```

The invariant is:

```text
available = on_hand - reserved
on_hand >= reserved >= 0
```

Quantities are positive integers in each item’s base unit, except signed adjustment deltas. Clients never edit balances directly.

### Endpoints

All endpoints use `/v1`.

| Method and path | Behavior |
|---|---|
| `POST /items` | Create an item. |
| `GET /items/{id}` | Retrieve an item. |
| `POST /locations` | Create a location. |
| `GET /locations/{id}` | Retrieve a location. |
| `GET /balances?item_id=…&location_id=…` | Query current balances. |
| `POST /receipts` | Add received stock. |
| `POST /adjustments` | Correct stock using signed deltas and a required reason. |
| `POST /transfers` | Move available stock between locations atomically. |
| `POST /reservations` | Reserve stock across one or more item/location pairs. |
| `GET /reservations/{id}` | Retrieve reservation status. |
| `POST /reservations/{id}/commit` | Ship reserved stock. |
| `POST /reservations/{id}/release` | Release reserved stock. |
| `GET /movements?item_id=…&location_id=…` | Read the stock audit trail. |

List endpoints use opaque cursor pagination with `limit` and `cursor`.

### Reservation workflow

```http
POST /v1/reservations
Authorization: Bearer …
Idempotency-Key: checkout-order-789
Content-Type: application/json
```

```json
{
  "reference": "order_789",
  "expires_at": "2026-10-23T10:45:00Z",
  "lines": [
    {
      "item_id": "itm_123",
      "location_id": "loc_456",
      "quantity": 3
    }
  ]
}
```

```http
HTTP/1.1 201 Created
Location: /v1/reservations/rsv_abc
```

```json
{
  "id": "rsv_abc",
  "status": "active",
  "reference": "order_789",
  "expires_at": "2026-10-23T10:45:00Z",
  "lines": [
    {
      "item_id": "itm_123",
      "location_id": "loc_456",
      "quantity": 3
    }
  ]
}
```

Creation increases `reserved`, reducing `available`. All lines succeed or fail together.

Reservations have four states:

```text
active → committed
active → released
active → expired
```

- **Commit:** decreases both `on_hand` and `reserved`; creates shipment movements.
- **Release or expiry:** decreases `reserved`; leaves `on_hand` unchanged.
- **Expired reservations cannot be committed**, even if background cleanup has not run yet.
- The initial API commits or releases the entire reservation. Partial fulfillment can be added when its requirements are clear.

### Stock changes

A receipt specifies a location and positive quantities:

```json
{
  "location_id": "loc_456",
  "external_reference": "delivery_1042",
  "lines": [
    { "item_id": "itm_123", "quantity": 20 }
  ]
}
```

An adjustment specifies signed deltas and a reason:

```json
{
  "location_id": "loc_456",
  "reason": "cycle_count",
  "lines": [
    { "item_id": "itm_123", "delta": -2 }
  ]
}
```

Reject adjustments that would reduce `on_hand` below `reserved`. Corrections create compensating movements; historical movements cannot be edited or deleted.

Transfers move available stock between locations immediately. Physical shipments that spend time in transit should use a separate transfer workflow before that capability launches.

### Reliability and concurrency

- **Atomic stock checks:** simultaneous requests cannot reserve or remove the same available units. A previously fetched balance does not guarantee a later reservation will succeed.
- **Idempotency:** require `Idempotency-Key` on mutation requests. Scope keys to the tenant and operation, retain results for seven days, and reject reuse with a different payload.
- **Business deduplication:** receipt references are unique within a tenant, preventing duplicate receipt ingestion beyond the idempotency window.
- **Consistent reads:** successful mutations are immediately reflected in balance and reservation reads.
- **Auditability:** movements record the actor, timestamp, reason, reference, and originating operation.

### Errors and access

Use RFC 9457 `application/problem+json` errors with stable machine-readable codes:

```json
{
  "type": "https://api.example.com/problems/insufficient-stock",
  "title": "Insufficient available stock",
  "status": 409,
  "code": "insufficient_stock",
  "detail": "Requested 3 units; 2 are available.",
  "item_id": "itm_123",
  "location_id": "loc_456"
}
```

Use `400` for malformed requests, `422` for invalid field values, `404` for missing resources, `409` for stock or state conflicts, and `429` with `Retry-After` for rate limits.

Authenticate service clients with OAuth 2.0 bearer tokens and scopes such as `inventory:read`, `inventory:write`, and `inventory:adjust`. Derive tenant access from credentials.

Publish an OpenAPI contract with examples and retry guidance. Keep `/v1` changes backward compatible; introduce a new major version for breaking behavior or schema changes.
