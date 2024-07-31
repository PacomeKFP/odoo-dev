## Exercise

Add business logic to the CRUD methods.

- Prevent deletion of a property if its state is not “New” or “Canceled”

  Tip: create a new method with the `ondelete()` decorator and remember that `self` can be a recordset with more than one record.

- At offer creation, set the property state to “Offer Received”. Also raise an error if the user tries to create an offer with a lower amount than an existing offer.

  Tip: the `property_id` field is available in the `vals`, but it is an `int`. To instantiate an `estate.property` object, use `self.env[model_name].browse(value)` ([example](#)).
  